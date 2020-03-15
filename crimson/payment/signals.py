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
    flag3=int(li[4])
    
    arr=["www", "com",]
    app_name=list(domain.split("."))
    for i in app_name:
        for j in arr:
            if i==j:
                app_name.remove(i)
    app=app_name[0]+".apk"
    print(domain,"domain===========================>1", emails)
    
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print(key, keystore, keystore_link, flag, flag3, "ok111111111111111111111111111111111111111")
        user_instance=CustomUser.objects.get(email=emails)
        apk=releaseapk.objects.create(domain_name=domain, app_name=app, user=user_instance)
        apk.save()
        apk2=get_object_or_404(releaseapk, domain_name=domain)
        apk2.paid=True
        apk2.save()
        
        if (flag==1 or flag3==0):
            keystore_data=keystore_table.objects.create(keystore=keystore, keystore_link=keystore_link, user=user_instance)
            keystore_data.save()
            print("flag===============1")
        else:
            keystore_data=get_object_or_404(keystore_table, keystore=keystore)
            keystore_data.keystore_link=keystore_link
            keystore_data.save()
            print("flag===============0")
        
        keystore_instance=keystore_table.objects.get(keystore=keystore)
        key_data=key_table.objects.create(key=key, keystore=keystore_instance)
        key_data.save()

        
        print(domain,"domain===========================>2")
       