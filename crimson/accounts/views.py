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

def index(request):
    return render(request,'accounts/index.html')

def debugapk_view(request):
    domain=None
    email_id=None
    if request.method == 'POST':
        form=request.POST
        domain = form['domain']
        email_id=form['email']
        arr=["www", "com",]
        app_name=list(domain.split("."))
        for i in app_name:
            for j in arr:
                if i==j:
                    app_name.remove(i)
        app=app_name[0]+".apk"

        if domain and email_id :
            receiver_mail=email_id
            file=open('app/crimson/src/main/res/raw/domain.txt', 'w')
            file.write(domain)
            file.close()
            print(domain, email_id)
            file=open('app/crimson/src/main/res/raw/domain.txt', 'r')
            text=file.readline()
            file.close()
            send_mail('Crimson Insight WebApp', text, 'sanjaykumarsupanch@gmail.com' ,[receiver_mail])

            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            os.system("./gradlew build")
            os.system("./gradlew assembleDebug")
            os.system("ls")
            os.system("cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
            link='http://'+request.get_host()+'/accounts/debug/'+app 
            
            send_mail('Crimson Insight WebApp', 'Hello!! Your WebApp dowload link here  %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
            os.chdir("../../")
            return redirect("/")
    return render(request, 'accounts/debugapk.html', {})

@login_required
def apk_data(request):
    if request.method == "POST":
        form1 = releaseForm(request.POST)
        
        domain_name=form1['domain_name'].value()
        key=form1['key'].value()
        
        request.session['domain_name']=domain_name
        request.session['key']=key
        
        if form1.is_valid():
            form1.save()
            apk=releaseapk.objects.get(domain_name=domain_name)
            apk.delete()
            return redirect("/payment/process/")
        
    else:
        form1 = releaseForm()
    
    return render(request, 'accounts/apk_data.html', {'form1': form1})



@login_required
def releaseapk_view(request):
    domain=request.session.get('domain_name')
    key =request.session.get('key')
    app=request.session.get('app')
    file=open('app/crimson/src/main/res/raw/domain.txt', 'w')
    file.write(domain)
    file.close()
    sleep(5)
    apk=releaseapk.objects.get(domain_name=domain)
    
    if (apk.paid == True):
        print("###############__Operating System Command__##################")
        os.system("ls")
        os.chdir("app/crimson/")
        os.system("keytool -genkeypair -v  -keystore signing.keystore -storepass qwerty -keyalg RSA -keysize 2048 -validity 10000  -alias %s -dname 'CN=CrimsonInsight, OU=SoftwareDeveloper, O=CrimsonInsight, L=Deo, S=Haryana, C=IN' qwerty" % (key))
        os.system("./gradlew build")
        os.system("./gradlew assembleRelease")
        os.system("ls")
        os.system("cp build/outputs/apk/release/crimson-release.apk ../../apk_store/release/%s" % app)
        link='http://'+request.get_host()+'/accounts/release/'+app 
        receiver_mail=str(request.user)
        print(link, "lllllllllliiiiiiiiiinnnnnnnnnnkkkkkkkkk")
        send_mail('Crimson Insight Sign WebApp', 'Hello!! Your WebApp dowload link here : %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
        os.chdir("../../")
        # return redirect('/payment/process/')
    else:
        return redirect('/accounts/payment/')
    return  render(request, 'accounts/releaseapk.html', {'form':receiver_mail})
            
def download_file_release(request, filename):
    fl_path='apk_store/release/'+filename
    fl=open(fl_path, 'rb')
    response = HttpResponse(fl, content_type="application/vnd.android.package-archive")
    response['Content-disposition'] = "attachment; filename=%s"%filename
    return response

def download_file_debug(request, filename):
    fl_path='apk_store/debug/'+filename
    fl=open(fl_path, 'rb')
    response = HttpResponse(fl, content_type="application/vnd.android.package-archive")
    response['Content-disposition'] = "attachment; filename=%s"%filename
    return response
