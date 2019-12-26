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
    # args={}
    host = request.get_host()
    print(host)
    # domain = request.META['HTTP_HOST']
    paypal_dict = {
    'business': settings.PAYPAL_RECEIVER_EMAIL,
    'amount': '100.00',
    'currency_code':'IN',
    'item_name': "CrimsonInsight",
    'invoice': "unique-invoice-00001",
    'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
    'return_url':'http://127.0.0.1/payment/done/',
    'cancel_return':'http://127.0.0.1/payment/canceled/',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    # args['form']=form
    return render(request, 'payment/process.html', {'form':form})


@csrf_exempt
def paypal_return(request):
    # args={'post':request.POST, 'get':request.GET}
    return render(request, 'payment/done.html')

@csrf_exempt
def paypal_cancel(request):
    # args={'post':request.POST, 'get':request.GET}
    return render(request, 'payment/canceled.html')

