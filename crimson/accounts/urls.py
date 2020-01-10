from django.urls import path, include
# from django_file_download import views as file_views
from .import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from accounts import views as user_views
from .views import *



app_name = "accounts"


urlpatterns = [
    path('register/', views.signup, name='register'),
    path('debugapk/', views.debugapk, name='debugapk'),
    path('releaseapk/', views.releaseapk, name='releaseapk'),
]