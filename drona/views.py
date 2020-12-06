from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
import json
import requests
from drona.models import Contest
from home.models import CustomUser

# Create your views here.
 
    
def data(URL):
    return requests.get(URL).json()

def home(request):
    return render(request, 'drona/index.html')

def isvalid_handle(handle):
    return 1
    

def guru_list(request):

    if request.is_ajax and request.method=='POST':
        guru = request.POST.get('guru_handle')
       
        if(isvalid_handle(guru)):
            request.Customuser.gurus = request.Customuser.gurus +';'+ guru
            return JsonResponse({"x":1})
        else:
            return JsonResponse({"x":0})

    else:
        return HttpResponse("ERROR")




def contests(request):
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
        if fetched_data['status']!='OK':
            return HttpResponse("Please enter Handles carefully")

        submissions_guru = fetched_data["result"]
        for submission in submissions_guru:
            if submission['author']['participantType']!='PRACTICE':
                guru_contests.add(submission["problem"]["contestId"])
        

    for id in guru_contests:
        if id in student_contests:
            print('https://codeforces.com/contest/'+str(id) , ' green')
        else :
            print('https://codeforces.com/contest/'+str(id) , ' red')

    # To be done
    # check if name retrieval possible using id in less time without api

    return render(request, 'drona/contests.html')


def problems(request):
    #from form
    gurus = ["coder_pulkit_c" , 'shivamsinghal1012']
    student = "Shashank_Chugh"

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
    
    for problem in guru_solved_list:
        if str(problem["contestId"])+problem['index'] in student_solved_set:
            print("https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index'] + ' GREEN' )
        else:
            print("https://codeforces.com/contest/"+str(problem["contestId"])+"/problem/"+problem['index'] + ' RED' )

    return render(request, 'drona/problems.html')
        
        


