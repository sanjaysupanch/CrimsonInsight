from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import *
from django.http import HttpResponseRedirect, HttpResponse, response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.models import *
from accounts.forms import *
import os
import smtplib
from django.core.mail import send_mail
from .utils import render_to_pdf
from django.views.generic import View
from django.template.loader import get_template
# from paypal.standard.models import *
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import dataSerializer
from rest_framework import permissions, status, generics, mixins
from .hooks import *


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
        user = request.user
        user_instance=CustomUser.objects.get(email=request.user)
        domain_data=releaseapk.objects.filter(user=user_instance)
        flag4=0
        flag5=0
        # print(list(domain.split('/')), "@@@@@@@@@@@@@@@@@@@@@@@@@@")
        dummy=["http:", "/", "https:"]
        data={}
        for i in range(2):
            if(dummy[i] in domain):
                flag5=1
                data={'flag5':flag5}
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return JsonResponse(data)

        for i in domain_data:
            if(domain in i.domain_name):
                flag4=1
                print(domain, i.domain_name, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                data={'flag4':flag4}
                return JsonResponse(data)
            elif(i.domain_name==domain):
                flag4=1
                data={'flag4':flag4}
                return JsonResponse(data)
            
            
        
        request.session['domain']=domain
        email_id = str(request.user)
        app=request.session.get('app')
        app = app+".apk"
        print("=====================2222====================")
        if domain:
            receiver_mail = email_id
            file = open('app/crimson/src/main/res/raw/domain.txt', 'w')
            file.write(domain)
            file.close()
            print("###############__Operating System Command__##################")
            os.system("ls")
            os.chdir("app/crimson/")
            os.system("./gradlew build")
            os.system("./gradlew assembleDebug")
            os.system("ls")
            os.system("cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
            link = 'http://'+request.get_host()+'/accounts/debug/'+app
            print("linkkk", link)
            send_mail('AppThisWeb WebApp', 'Hello!! Your Debug WebApp dowload link is here  %s' %
                      link, 'pioneer.deo@gmail.com', [receiver_mail])
            os.chdir("../../")
            return redirect("/dashboard/debugapk/")
            # return HttpResponse('')
    return HttpResponse('')

# @login_required
# def debugapk_view1(request):
#     domain=request.session.get('domain')
#     email_id=request.user
#     app=request.session.get('app')
#     app = app+".apk"   
#     if domain:
#         receiver_mail = email_id
#         file = open('app/crimson/src/main/res/raw/domain.txt', 'w')
#         file.write(domain)
#         file.close()
#         # sasasa
#         print("###############__Operating System Command__##################1")
#         os.system("ls")
#         os.chdir("app/crimson/")
#         os.system("./gradlew build")
#         os.system("./gradlew assembleDebug")
#         os.system("ls")
#         os.system("cp build/outputs/apk/debug/crimson-debug.apk ../../apk_store/debug/%s" % app)
#         link = 'http://'+request.get_host()+'/accounts/debug/'+app
#         print("linkkk", link)
#         send_mail('Crimson Insight WebApp', 'Hello!! Your Debug WebApp dowload link is here  %s' %
#                     link, 'pioneer.deo@gmail.com', [receiver_mail])
#         os.chdir("../../")
#         return redirect("/dashboard/debugapk/")
            # return HttpResponse('')

def session_data(request):
    
    if request.method == "POST":
        form = request.POST
        domain = form['domain']
        keystore = form['keystore']
        keystore_pass = form['keystore_pass']
        print("===========================================1")
        key = form['key']
        key_pass=form['key_pass']
        key_user_name=form['key_user_name']
        key_organization_unit=form['key_organization_unit']
        key_organization=form['key_organization']
        key_city=form['key_city']
        key_state=form['key_state']
        key_country=form['key_country']
        app=request.session.get('app')
        temp_data=temp.objects.create(keystore=keystore, keystore_pass=keystore_pass, key=key, key_pass=key_pass)
        temp_data.save()
        flag = 1; flag2 = 1; flag3 = 1
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

        key_data = {'domain':domain, 'keystore':keystore,'keystore_pass':keystore_pass,'key':key, 'key_pass':key_pass, 'key_user_name':key_user_name,'key_organization_unit': key_organization_unit, 'key_organization':key_organization, 'key_city': key_city,'key_state': key_state, 'key_country': key_country, 'app':app, 'flag':flag, 'flag3':flag3 }
        
        request.session['key_data']=key_data
        
        data = {'flag': flag, 'flag3': flag3,}
        return JsonResponse(data)

    return HttpResponse('')

@login_required
def key_data(request):
    if request.method=="POST":
        form=request.POST
        keystore=form['keystore']
        print("111111111111", keystore)
        request.session['keystore1']=keystore
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

@login_required
def update(request):
    if request.method=='POST':
        form= request.POST
        app_name=form['app_name']
        request.session['app_name']=app_name
        # print(app_name, "2222222222222222222222222222222222")
        # redirect('/dashboard/update_app/update_app/')
    return HttpResponse('')

@login_required
def update_app(request):
    return render(request, 'dashboard/update_app.html', {})
    
@login_required
def app_builded(request):
    app_name=request.session.get('app_name')
    app=request.session.get('app') #updated name
    app=app+".apk"

    user_instance=CustomUser.objects.get(email=request.user)
    app_and_keys=app_and_keystore.objects.get(user=user_instance, app_name=app_name)    
    keystore=app_and_keys.keystore
    app_and_keys.app_name=app
    app_and_keys.save()

    apk_data=releaseapk.objects.get(app_name=app_name, user=user_instance)
    apk_data.app_name=app
    apk_data.save()

    keystore_data=keystore_table.objects.get(keystore=keystore)
    keystore_pass=keystore_data.keystore_pass

    key_data=key_table.objects.get(keystore=keystore_data)
    key=key_data.key
    key_pass=key_data.key_pass
    
    temp.objects.create(keystore=keystore, keystore_pass=keystore_pass, key=key, key_pass=key_pass)

    os.chdir("app/crimson/")
    os.system("./gradlew build")
    os.system("./gradlew assembleRelease")
    os.system("ls")
    os.system("cp build/outputs/apk/release/crimson-release.apk ../../apk_store/release/%s" % app)
    os.system("cp build/outputs/apk/release/crimson-release.apk ../../apk_store/debug/%s" % app)
    link='http://'+request.get_host()+'/accounts/release/'+app 
    receiver_mail=str(request.user)
    print(link)
    send_mail('AppThisWeb Sign WebApp', 'Hello!! Your sign WebApp download link here : %s' % link, 'sanjaykumarsupanch@gmail.com', [receiver_mail])
    os.chdir("../../")
    #temp.objects.all().delete()
    
    return HttpResponse('')


@login_required
def file_upload(request):
    os.chdir("media/icon/")
    os.system("rm -rf *")
    os.chdir("../../")
    img_path=""
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            app=form['app_name'].value()
            app=app.lower()
            app_icon=str(form['app_icon'].value())
            app_label(app)
            request.session['app'] = app
            print(app, "appppppppppppppppppppppppppppppppppppppp")
            
            if len(request.FILES) == 0:
                os.chdir("app/crimson/src/main/res/drawable-hdpi/")
                os.system('rm -rf *')
                os.chdir("../../../../../../")
                os.system("cp media/default/logo.png app/crimson/src/main/res/drawable-hdpi/logo.png")
                img_path="../../media/default/logo.png"
            
            else:
                li=list(app_icon.split("."))
                app_icon1=li[0]
                app_icon2=li[1]
                icon="logo."+app_icon2
                # os.system("ls")
                os.chdir("app/crimson/src/main/res/drawable-hdpi/")
                os.system('rm -rf *')
                os.chdir("../../../../../../")
                os.system("cp media/icon/%s app/crimson/src/main/res/drawable-hdpi/%s" % (app_icon, icon))
                img_path="../../media/icon/%s" % (app_icon)
            appname_and_image.objects.all().delete()
            data={'app_name':app, 'app_icon':img_path}
            
            return JsonResponse(data)
    else:
        form=documentForm()
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
    