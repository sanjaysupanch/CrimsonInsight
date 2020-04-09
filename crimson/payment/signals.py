from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from accounts.models import *
 
@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn_obj = sender
    data=ipn_obj.custom
    data=list(data.split(' '))
    domain=data[0]
    app=data[1]
    email=data[2]
    print(domain, app, email)
    
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        user_instance=CustomUser.objects.get(email=email)
        apk=releaseapk.objects.create(domain_name=domain, app_name=app, user=user_instance)
        apk.save()
        apk2=get_object_or_404(releaseapk, domain_name=domain)
        apk2.paid=True
        apk2.save()    
        print("Payment singnal receive successfully===========================>1")
       