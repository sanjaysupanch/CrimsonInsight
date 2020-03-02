from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import *
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from accounts.models import *
import os
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import mimetypes
from random import randint
from django.core.mail import send_mail
from time import sleep
count2=1

@login_required
def index(request):
    data=keystore_table.objects.all()
    return render(request,'dashboard/index.html', {'data':data})

@login_required
def converted_app(request):
    data=releaseapk.objects.all()
    return render(request,'dashboard/converted_app.html', {'data':data})

@login_required
def keystore(request):
    data=keystore_table.objects.all()
    return render(request,'dashboard/keystore.html', {'data':data})

@login_required
def billing(request):
    return render(request,'dashboard/billing.html')

@login_required
def debugapk_view(request):
    
    if request.method == 'POST':
        form=request.POST
        domain = form['domain']
        email_id=request.user
        
        print("==========>Spliting app name<=============")
        arr=["www", "com"]
        app_name=list(domain.split("."))
        for i in app_name:
            for j in arr:
                if i==j:
                    app_name.remove(i)
        app=app_name[0]+".apk"           
        request.session['app']=app
        print("===========>Ending app name<=============")

        if domain:
            receiver_mail=email_id
            file=open('app/crimson/src/main/res/raw/domain.txt', 'w')
            file.write(domain)
            file.close()
            print(domain, email_id)
            file=open('app/crimson/src/main/res/raw/domain.txt', 'r')
            text=file.readline()
            file.close()
            print("ssssssssss", text)
            #send_mail('Crimson Insight WebApp', text, 'sanjaykumarsupanch@gmail.com' ,[receiver_mail])
            print("sssssss", text)
            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            os.system("./gradlew build")
            os.system("./gradlew assembleDebug")
            os.system("ls")
            os.system("cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
            link='http://'+request.get_host()+'/accounts/debug/'+app 
            print("linkkk", link)
            #send_mail('Crimson Insight WebApp', 'Hello!! Your WebApp dowload link here  %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
            os.chdir("../../")
            return redirect("/dashboard/debugapk/")
    return HttpResponse('')

def session_data(request):
    if request.method =="POST":
        form=request.POST
        domain=form['domain']
        keystore=form['keystore']
        key=form['key']
        flag=0
        key_data=keystore_table.objects.all()
        
        for i in key_data:
            if(i.keystore==keystore):
                flag=0
                break
            else:
                flag=1
        
        request.session['flag']=flag
        request.session['domain_name']=domain
        request.session['key']=key
        request.session['keystore']=keystore
        print("**********************=>", domain, keystore, key)
    return HttpResponse('')


def download_keystore(request, filename):
    fl_path='app/crimson/'+filename
    fl=open(fl_path, 'rb')
    response = HttpResponse(fl, content_type="application/vnd.android.package-archive")
    response['Content-disposition'] = "attachment; filename=%s"%filename
    return response

# def download_file_debug(request, filename):
#     fl_path='apk_store/debug/'+filename
#     fl=open(fl_path, 'rb')
#     response = HttpResponse(fl, content_type="application/vnd.android.package-archive")
#     response['Content-disposition'] = "attachment; filename=%s"%filename
#     return response
