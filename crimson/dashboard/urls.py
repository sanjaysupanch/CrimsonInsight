from django.urls import path
from .import views 
from django.conf.urls import url
from dashboard.views import *
# from rest_framework import views



urlpatterns = [
    
    path('', views.index, name='index'),
    path('converted_app/', views.converted_app, name='converted_app'),
    path('keystore/', views.keystore, name='keystore'),
    path('billing/', views.billing, name='billing'),
    path('debugapk/', views.debugapk_view, name="debugapk"),
    path('data/', views.session_data, name="session_data"),
    path('<filename>/', views.download_keystore, name="keystore_file"),
    path('pdf/pdf/', views.genrate, name="pdf"),
    path('pdf/data/', views.pdf_get_data, name="pdf_data"),
    path('keydata/data/', KeydataView.as_view(), name="data"),

]