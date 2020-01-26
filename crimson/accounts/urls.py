from django.urls import path, include
# from django_file_download import views as file_views
from .import views 
# from django.contrib.auth import views as auth_views
from django.conf.urls import url
# from accounts import views as user_views
from .views import *



# app_name = "accounts"


urlpatterns = [
    # path('register/', views.signup, name='register'),
    path('debugapk/', views.debugapk_view, name='debugapk'),
    path('releaseapk/', views.releaseapk_view, name='releaseapk'),
    path('payment/', views.apk_data, name="apk_data"),
    path('release/<filename>/', views.download_file_release, name="download_file"),
    path('debug/<filename>/', views.download_file_debug, name="download_file"),
    
]