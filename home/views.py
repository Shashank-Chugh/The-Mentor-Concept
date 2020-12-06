from django.shortcuts import render,HttpResponse,redirect
import json
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def data(URL):
    return requests.get(URL).json()

def signup(request):
    if request.method == 'POST':
        handle = request.POST['handle']
        email = request.POST['email']
        password = request.POST['password']
        
        #use api to get more info
        fetched_data = data("https://codeforces.com/api/user.info?handles="+handle)
        
        if fetched_data['status'] !='OK':
            return HttpResponse("ERROR")
        fetched_data = fetched_data['result'][0]

        photoURL = fetched_data['titlePhoto']
        user = User.objects.create_user(handle,email,password)

        customUser =CustomUser(photoURL=photoURL , user=user)
        customUser.save()

        return redirect('/')
    else:
        return HttpResponse("Error")

        # Check handle !! and show error i not found 


def login_fn(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpassword']
        
        user = authenticate(username=username , password=password )

        if user is not None:
            login(request,user)
            print('welcome ' + user.username)
            return redirect('/drona')
        else:
            return HttpResponse('No user found')


    else:
        return HttpResponse("Error")

def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        return HttpResponse("Error")