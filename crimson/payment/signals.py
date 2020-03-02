from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from accounts.models import *
 
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    domain=ipn_obj.invoice
    strings=ipn_obj.custom
    li=list(strings.split(" "))
    key=str(li[0])
    emails=str(li[1])
    keystore=str(li[2])
    keystore_link="/dashboard/"+keystore+".keystore"
    flag=int(li[3])
    
    arr=["www", "com",]
    app_name=list(domain.split("."))
    for i in app_name:
        for j in arr:
            if i==j:
                app_name.remove(i)
    app=app_name[0]+".apk"
    # keystore_data=keystore_table.objects.all()



    print(domain,"domain===========================>1")
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print("ok111111111111111111111111111111111111111")
        user_instance=CustomUser.objects.get(email=emails)
        
        if (flag==1):
            keystore_data=keystore_table.objects.create(keystore=keystore, keystore_link=keystore_link, key=key, user=user_instance)
            keystore_data.save()
            print("flag===============1")
        else:
            keystore_data=get_object_or_404(keystore_table, keystore=keystore)
            keystore_data.key=key
            keystore_data.keystore_link=keystore_link
            keystore_data.save()
            print("flag===============0")
        
        apk=releaseapk.objects.create(domain_name=domain, key=key, keystore=keystore, keystore_link=keystore_link, app_name=app, user=user_instance)
        apk.save()
        print("ok2222222222222222222222222222222222222222")
        apk2=get_object_or_404(releaseapk, domain_name=domain)
        apk2.paid=True
        apk2.save()
        print(domain,"domain===========================>2")
       