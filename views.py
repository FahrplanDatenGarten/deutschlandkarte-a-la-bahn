from django.shortcuts import render
from django.urls import path

from . import views

app_name = 'netzkarte'
urlpatterns = [
    path('netzkarte', views.gtfsexport, name='netzkarte')
]
