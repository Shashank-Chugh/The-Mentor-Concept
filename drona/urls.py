from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home , name='home_drona'),
    path('problems/', views.problems , name='problems_drona'),
    path('contests/', views.contests , name='contests_drona'),
    path('guru_list/', views.guru_list , name='guru_list'),

]
