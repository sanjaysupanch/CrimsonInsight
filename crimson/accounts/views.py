from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import *
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import *
import os
import smtplib 
from django.core.mail import send_mail
from time import sleep


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
            
            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            os.system("./gradlew build")
            os.system("./gradlew assembleDebug")
            os.system("ls")
            os.system("cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
            link='http://'+request.get_host()+'/accounts/debug/'+app 
            
            send_mail('Crimson Insight WebApp', 'Hello!! Your Debug WebApp dowload link here  %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
            os.chdir("../../")
            sleep(5)
            return redirect("/accounts/login/")
    return render(request, 'accounts/debugapk.html', {'email':email_id})

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
    
    keystore1=request.session.get('keystore1')
    domain=request.session.get('domain')
    app=request.session.get('app')+".apk"
    key_data=request.session.get('key_data')
    if(key_data==None):
        key_data={}
    
    file=open('app/crimson/src/main/res/raw/domain.txt', 'w')
    file.write(domain)
    file.close()
    
    if(keystore1 !=None):
        key_data['flag']=0
        key_data['flag3']=0
    sleep(5)
    
    apk=releaseapk.objects.get(domain_name=str(domain))
    if (apk.paid==True):
        print("###############__Operating System Command__##################")
        os.system("ls")
        os.chdir("app/crimson/")
        if(key_data['flag']==1 or key_data['flag3']==1):
            os.system("keytool -genkey -v -keystore %s -storepass %s -alias %s -keypass %s -keyalg RSA -keysize 2048 -validity 10000 -dname 'CN=%s, OU=%s, O=%s, L=%s, S=%s, C=%s'" % (key_data['keystore']+".keystore", key_data['keystore_pass'], key_data['key'], key_data['key_pass'], key_data['key_user_name'], key_data['key_organization_unit'], key_data['key_organization'], key_data['key_city'], key_data['key_state'], key_data['key_country']))
            user_instance=CustomUser.objects.get(email=request.user)
            keystore_link="/dashboard/"+key_data['keystore']+".keystore"
            keystore_table.objects.create(keystore=key_data['keystore'], keystore_pass=key_data['keystore_pass'], keystore_link=keystore_link, user=user_instance)
            keystore_instance=keystore_table.objects.get(keystore=key_data['keystore'])
            key_table.objects.create(keystore=keystore_instance, key=key_data['key'], key_pass=key_data['key_pass'], key_user_name=key_data['key_user_name'], key_organization_unit=key_data['key_organization_unit'], key_organization=key_data['key_organization'],key_city= key_data['key_city'], key_state=key_data['key_state'], key_country=key_data['key_country'])
        else:
            
            keystore_instance=keystore_table.objects.get(keystore=keystore1)
            data=key_table.objects.get(keystore=keystore_instance)
            keystore_name=keystore_instance.keystore
            keystore_pass=keystore_instance.keystore_pass
            key=data.key
            key_pass=data.key_pass
            temp.objects.create(keystore=keystore1, keystore_pass=keystore_pass, key=key, key_pass=key_pass)
        
        os.system("./gradlew build")
        os.system("./gradlew assembleRelease")
        os.system("ls")
        os.system("cp build/outputs/apk/release/crimson-release.apk ../../apk_store/release/%s" % app)
        link='http://'+request.get_host()+'/accounts/release/'+app 
        receiver_mail=str(request.user)
        print(link)
        send_mail('Crimson Insight Sign WebApp', 'Hello!! Your sign WebApp download link here : %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
        os.chdir("../../")
        temp.objects.all().delete()
        # request.session.flush()
        # return redirect('/payment/process/')
    else:
        return redirect('/payment/done/')
    return  render(request, 'accounts/releaseapk.html', {'email':receiver_mail})
            
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

