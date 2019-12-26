from django.urls import path, include
from .import views 
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from .views import *



app_name = "payment"


urlpatterns = [
    path('process/', views.payment, name='process'),
    path('done/', views.paypal_return, name='done'),
    path('canceled/', views.paypal_cancel, name='canceled'),

]