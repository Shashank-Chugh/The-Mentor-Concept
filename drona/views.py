from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
import requests
from drona.models import Contest
from django.core.paginator import Paginator

# Create your views here.
                  
    
def data(URL):
    return requests.get(URL).json()

def getCat():
    return [ 
        ['2-sat'   ,  'binary search' ,    'bitmasks'   ,  'brute force'  ,   'chinese remainder theorem'     ,'combinatorics'  ,   'constructive algorithms',     'data structures'  ,   'dfs and similar' ,'probabilities'  ,   'schedules'   ,  'shortest paths' ]  ,                        
        
        ['divide and conquer'   ,  'dp' ,    'dsu'    , 'expression parsing'   ,  'fft'  ,   'flows'  ,   'games'     ,'geometry'  ,   'graph matchings',   'sortings' ,    'string suffix structures'     ,'strings']
        ,
        ['graphs'  ,   'greedy'  ,   'hashing'  ,   'implementation'  ,   'interactive' ,    'math'  ,   'matrices'     ,'meet-in-the-middle'  ,   'number theory' ,   'ternary search'   ,  'trees'     ,'two pointers'],
    
               ]

def home(request):
    gurus = list( request.user.profile.gurus.split(' '))
    categories = getCat()

    context =   {  "gurus" : gurus  ,  "categories":categories}
    return render(request, 'drona/index.html',context)

def isvalid_handle(handle):
    return 1
    

def guru_list(request):

    if request.is_ajax and request.method=='POST':
        guru = request.POST.get('guru_handle')
       
        if(isvalid_handle(guru)):
            print(request.user.profile.gurus)
            request.user.profile.gurus = request.user.profile.gurus + guru+' '
            request.user.save()
            print(request.user.profile.gurus)
            return JsonResponse({"x":1})
        else:
            return JsonResponse({"x":0})

    elif request.is_ajax:
        s=request.user.profile.gurus.strip()
        guru_handles = s.split(' ')
        return JsonResponse( { "guru_handles" : guru_handles  }  )

    else:
        return HttpResponse("ERROR_guru_list")

def delete_guru(request):
    if request.is_ajax and request.method=='POST':
        guru = request.POST.get('guru_handle')
       
        if guru in request.user.profile.gurus:
            print(request.user.profile.gurus)
            start  = request.user.profile.gurus.index(guru)
            end = start + len(guru)

            request.user.profile.gurus = request.user.profile.gurus[:start] + request.user.profile.gurus[end+1:]
            request.user.save()
            print(request.user.profile.gurus)

            return JsonResponse(  { 'x':1 } )
        else:
            return HttpResponse('ERROR_delete_guru')
    else:
        return HttpResponse("ERROR_delete_guru")



def contests_data(request):
    #handles from form
    gurus = ["coder_pulkit_c" , 'shivamsinghal1012']

    #assumption student handle is correct here , already checked during login
    student = "Shashank_Chugh"

    #fetch from api
    submissions_student = data("https://codeforces.com/api/user.status?handle="+student)["result"]
    guru_contests=set()
    student_contests=set()

    for submission in submissions_student:
        if submission['author']['participantType']!='PRACTICE':
            student_contests.add(submission["problem"]["contestId"])

    for guru in gurus:
        fetched_data = data("https://codeforces.com/api/user.status?handle="+guru)
     
        submissions_guru = fetched_data["result"]
        for submission in submissions_guru:
            if submission['author']['participantType']!='PRACTICE':
                guru_contests.add(submission["problem"]["contestId"])
        

    contests_data=[]
    sno=1
    for id in guru_contests:
        if id not in student_contests:
            link= "https://codeforces.com/contest/"+str(id)
            contests_data.append({'sno':sno,'id':id,'link':link})
            sno+=1

    # To be done
    # check if name retrieval possible using id in less time without api
    context = { "contests_data" :contests_data }
    return JsonResponse( context  )

def contests(request):
     return render(request, 'drona/contests.html')





def problems_data(request):
    #from form
    # gurus = request.user.profile.gurus
    # gurus = gurus.strip()
    # gurus = gurus.split(' ')
    gurus = ['coder_pulkit_c']
    student = "Shashank_Chugh"

    tag_form = request.POST

    #fetch student submissions from api
    submissions_student = data("https://codeforces.com/api/user.status?handle="+student)["result"]

    student_solved_set = set()
    guru_solved_set = set()
    guru_solved_list = []

    for guru in gurus:
        fetched_data =data("https://codeforces.com/api/user.status?handle="+guru)
        if fetched_data['status']!='OK':
            return HttpResponse("ERROR")
        submissions_guru = fetched_data["result"]
        for submission in submissions_guru:
            if str(submission["problem"]['contestId'])+submission["problem"]['index'] in guru_solved_set:
                continue
            elif submission['verdict']=='OK':
                guru_solved_set.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])
                guru_solved_list.append(submission["problem"])

    for submission in submissions_student:
        if submission['verdict']=='OK':
            student_solved_set.add(str(submission["problem"]['contestId'])+submission["problem"]['index'])
    
    problems_data=[]
    sno=0
    for problem in guru_solved_list:
        
        if str(problem["contestId"])+problem['index'] not in student_solved_set:
            # problems_data.append(str(problem["contestId"])+"/problem/"+problem['index'] ) 
            # problems_name.append(problem['name'])  
            # print("https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index'] + ' RED' )
            sno+=1
            link = "https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index']
            rating  = "" 
            if 'rating' in problem:
                rating = problem["rating"]
            problems_data.append(  { 'sno':sno ,'name':problem['name'] , 'rating':rating , 'link':link }           )


    # problems_data =  Paginator(problems_data,50)
    # page_no = request.GET.get('page') or 1 
    # problems_data = problems_data.get_page(page_no)

    # problems_link =  Paginator(problems_link,10)
    # page_no = request.GET.get('page') 
    # problems_link = problems_link.get_page(page_no)

    context = { 'problems_data':problems_data }
    return JsonResponse(context) 

def problems(request):
    return render(request , 'drona/problems.html' )

        


