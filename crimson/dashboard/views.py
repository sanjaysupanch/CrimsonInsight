from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import *
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import *
import os
import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# import mimetypes
from django.core.mail import send_mail
from .utils import render_to_pdf
from django.views.generic import View
from django.template.loader import get_template
# from paypal.standard.models import *
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import dataSerializer
from rest_framework import permissions, status, generics, mixins
# from rest_framework.decorators import api_view

@login_required
def index(request):
    user = request.user
    user_instance = CustomUser.objects.get(email=request.user)
    data = keystore_table.objects.filter(user=user_instance)
    return render(request, 'dashboard/index.html', {'data': data, 'user': user})


@login_required
def converted_app(request):
    user_instance = CustomUser.objects.get(email=request.user)
    data = releaseapk.objects.filter(user=user_instance)
    return render(request, 'dashboard/converted_app.html', {'data': data})


@login_required
def keystore(request):
    user_instance = CustomUser.objects.get(email=request.user)
    data = keystore_table.objects.filter(user=user_instance)
    return render(request, 'dashboard/keystore.html', {'data': data})


@login_required
def billing(request):
    user_instance = CustomUser.objects.get(email=request.user)
    data = releaseapk.objects.filter(user=user_instance)
    return render(request, 'dashboard/billing.html', {'data': data})


@login_required
def debugapk_view(request):
    if request.method == 'POST':
        form = request.POST
        domain = form['domain']
        email_id = str(request.user)

        print("==========>Spliting app name<=============")
        arr = ["www", "com"]
        app_name = list(domain.split("."))
        for i in app_name:
            for j in arr:
                if i == j:
                    app_name.remove(i)
        app = app_name[0]+".apk"
        request.session['app'] = app
        print("===========>Ending app name<=============")
        user = request.user
        # user=CustomUser.objects.get(email=user)
        print(user.username)
        print("=========================================")
        if domain:
            receiver_mail = email_id
            file = open('app/crimson/src/main/res/raw/domain.txt', 'w')
            file.write(domain)
            file.close()
            print(domain, email_id)
            file = open('app/crimson/src/main/res/raw/domain.txt', 'r')
            text = file.readline()
            file.close()
            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            os.system("./gradlew build")
            os.system("./gradlew assembleDebug")
            os.system("ls")
            os.system(
                "cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
            link = 'http://'+request.get_host()+'/accounts/debug/'+app
            print("linkkk", link)
            send_mail('Crimson Insight WebApp', 'Hello!! Your Debug WebApp dowload link is here  %s' %
                      link, 'pioneer.deo@gmail.com', [receiver_mail])
            os.chdir("../../")
            return redirect("/dashboard/debugapk/")
    return HttpResponse('')


def session_data(request):
    if request.method == "POST":
        form = request.POST
        domain = form['domain']
        keystore = form['keystore']
        key = form['key']
        # user_instance=CustomUser.objects.get(email=request.user)
        temp_data=temp.objects.create(keystore=keystore, key=key)
        temp_data.save()
        flag = 1
        flag2 = 1
        flag3 = 1
        keystore_data = keystore_table.objects.all()
        for i in keystore_data:
            if(i.keystore == None):
                flag3 = 0
                break
            elif(i.keystore == keystore):
                flag = 0
                break
            else:
                flag = 1
                flag3 = 1
        request.session['flag'] = flag
        request.session['domain_name'] = domain
        request.session['key'] = key
        request.session['keystore'] = keystore
        request.session['flag3'] = flag3
        key_data = key_table.objects.all()
        if(flag == 0):
            for i in key_data:
                if(i.key == key):
                    flag2 = 0
                    break
                else:
                    flag2 = 1
        data = {
            'flag': flag,
            'flag2': flag2,
            'flag3': flag3,
        }
        return JsonResponse(data)

    return HttpResponse('')


@login_required
def download_keystore(request, filename):
    fl_path = 'app/crimson/'+filename
    fl = open(fl_path, 'rb')
    response = HttpResponse(
        fl, content_type="application/vnd.android.package-archive")
    response['Content-disposition'] = "attachment; filename=%s" % filename
    return response


@login_required
def genrate(request):
    invoice = request.session.get('invoice')
    user = request.user
    data = releaseapk.objects.get(invoice=int(invoice))
    date = data.date
    template = get_template('dashboard/invoice.html')
    context = {
        "invoice_no": str(invoice),
        "user": str(user),
        "username": str(user.username),
        "date": str(date),
    }
    html = template.render(context)
    pdf = render_to_pdf('dashboard/invoice.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


@login_required
def pdf_get_data(request):
    if request.method == 'POST':
        form = request.POST
        invoice = form['invoice']
        request.session['invoice'] = invoice
        redirect('/dashboard/pdf/pdf/')
    return HttpResponse('')


class KeydataView(generics.ListAPIView):
    queryset= temp.objects.all()
    serializer_class=dataSerializer

    def get_queryset(self):
        tempdata=temp.objects.all()
        last = tempdata[len(tempdata) - 1] if tempdata else None
        return temp.objects.filter(id=last.id)





# @api_view()
# def KeydataView(request):
#     keystore=None
#     key=None 
#     if(keystore==None and key==None):
#         print("step==1")
#         user_instance=CustomUser.objects.get(email=request.user)
#         temp_data=temp.objects.get(user=user_instance)
#         print("step==2")
#         keystore=temp_data.keystore
#         key=temp_data.key
#         print("step==3")
#     else:
#         print(keystore, key, "11111111")
#     # except:
#     #     print('222222222222')
#     # if(keystore==None and key == None):
#     #     keystore='signing'
#     #     key='qwerty'
    
#     print(keystore, key)
#     return Response([{"keystore": keystore, "key": key}])
    