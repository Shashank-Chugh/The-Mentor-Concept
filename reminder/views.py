from django.shortcuts import render,HttpResponse
from django.core.mail import send_mail
# Create your views here.


def home(request):
    res = send_mail("hello shashank", "How are You?", "shshankchugh3@gmail.com", ['shshankchugh2@gmail.com','mlbasic101@gmail.com'])
    return HttpResponse('%s'%res)