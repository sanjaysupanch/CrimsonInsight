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
    print(domain,"domain===========================>1")

    if ipn_obj.payment_status == ST_PP_COMPLETED:

        apk=releaseapk.objects.create(domain_name=domain, key=key, email_field=emails)
        apk.save()
        apk2=get_object_or_404(releaseapk, domain_name=domain)
        apk2.paid=True
        apk2.save()
        print(domain,"domain===========================>2")
       