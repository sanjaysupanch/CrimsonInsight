from django.urls import path
from .import views 
from django.conf.urls import url
from .views import *


urlpatterns = [
    
    path('', views.index, name='index'),
    path('converted_app/', views.converted_app, name='converted_app'),
    path('keystore/', views.keystore, name='keystore'),
    path('billing/', views.billing, name='billing'),
    path('debugapk/', views.debugapk_view, name="debugapk"),
    path('data/', views.session_data, name="session_data"),
    path('<filename>/', views.download_keystore, name="keystore_file"),
    
]