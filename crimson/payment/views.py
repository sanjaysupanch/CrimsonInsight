from django.shortcuts import render,render_to_response
from django.conf import settings
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.urls import reverse

@login_required
def payment(request):
    host = request.get_host()
    print("@@@@@@@@@",host)
    domain = request.META['HTTP_HOST']
    print(domain, "222222222222222")
    paypal_dict = {
    'business': settings.PAYPAL_RECEIVER_EMAIL,
    'amount': '0.10',
    'currency_code':'INR',
    'item_name': "CrimsonInsight",
    'invoice': "unique-invoice-id",
    'notify_url':'http://'+domain+'/payment/paypal/',
    'return_url':'http://'+domain+'/payment/done/',
    'cancel_return':'http://'+domain+'/payment/canceled/',
    }

    print("aaaaaaa", paypal_dict)
    form = PayPalPaymentsForm(initial=paypal_dict)
    # print(form)
    return render(request, 'payment/process.html', {'form':form})


@csrf_exempt
def paypal_return(request):
    args={'post':request.POST, 'get':request.GET}
    print("ssssssssssssss")
    return render(request, 'payment/done.html', args)

@csrf_exempt
def paypal_cancel(request):
    args={'post':request.POST, 'get':request.GET}
    print("ssssssssssssss")
    return render(request, 'payment/cancelled.html', args)