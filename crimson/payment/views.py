from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from .models import *
from accounts.forms import *


def process_payment(request):
    domain=request.session.get('domain_name')
    key = request.session.get('key')
    print("1111111110", domain, key)
    emails=str(request.user)
    strings= key+" "+emails
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '29.00',
        'item_name': 'Order',
        'invoice': domain,
        'currency_code': 'USD',
        'custom':strings,
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'form':form})

@csrf_exempt
def payment_done(request):
    return redirect('/accounts/releaseapk/')
    # return render(request, 'payment/payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment_cancelled.html')

