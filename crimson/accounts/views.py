from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import *
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import *
import os


def index(request):
    return render(request,'accounts/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def apkkey(request):
    if request.method == 'POST':
        form = apkForm(request.POST)
        domain = form['domain_name'].value()
        file=open('app/crimson/src/main/res/raw/domain.txt', 'w')
        file.write(domain)
        file.close()
        # print(form.data['key'])
        if form.is_valid():
            form.save()
            key = form.cleaned_data['key']
            print(key)
            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            
            os.system("keytool -genkeypair -v  -keystore signing.keystore -storepass qwerty -keyalg RSA -keysize 2048 -validity 10000  -alias %s -dname 'CN=CrimsonInsight, OU=SoftwareDeveloper, O=CrimsonInsight, L=Deo, S=Haryana, C=IN' qwerty" % (key))
            os.system("./gradlew build")
            os.system("./gradlew assembleRelease")
            
            with open("build/outputs/apk/release/crimson-release.apk", 'rb') as fh:
                response = HttpResponse(fh, content_type="application/vnd.android.package-archive") 
                response["Content-disposition"] = "attachment; filename={}".format(os.path.basename("build/outputs/apk/release/crimson-release.apk"))

            os.chdir("../../")
            

            return  response
    
    else:
        form = apkForm()
    return render(request, 'accounts/apk.html', {'form': form})


