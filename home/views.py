from django.shortcuts import render,HttpResponse
import json
import time
import urllib.request
# Create your views here.

def home(request):

    URL = 'https://codeforces.com/api/contest.list'
    with urllib.request.urlopen(URL) as url:
		    contests = json.loads(url.read().decode())["result"]
    
    cur_time = time.time()
    future_contests =[]
    for contest in contests:
        end_time = contest["startTimeSeconds"] +contest["durationSeconds"]
        if end_time>=cur_time:
            future_contests.append(contest) 
    context = { "future_contests":future_contests }
    return render(request, 'home/home.html',context)


