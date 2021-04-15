from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Price, Quarter_service, Transfer

# Create your views here.


@login_required
def index(request):
    ctx = {
        "new_requests": Quarter_service.objects.all().order_by('-timestamp')
    }
    return render(request, 'quarter/index.html', ctx)


def create_request(request):
    if request.method == "POST":
        name = request.POST['customername']
        phone = request.POST['phone']
        location = request.POST['address']
        email = request.POST['email']
        notes = request.POST['notes']
        new_request = Quarter_service(
            name=name, phone=phone, location=location, email=email, notes=notes, created_by=request.user)
        new_request.save()
        messages.success(request, "تم تسجيل طلبك بنجاح")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def request_details(request, id):
    req = Quarter_service.objects.get(pk=id)
    return render(request, 'quarter/request_details.html', {'req': req})


def pricing(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        price = request.POST['price']
        files = request.FILES['files']
        notes = request.POST['notes']

        price = Price(service=req, price=price, files=files,
                      notes=notes, created_by=request.user)
        price.save()
        req.pricing = price
        req.status = "pending price review"
        req.save()

        messages.success(request, "تم ارسال السعر .")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirm_process(request, id):
    """
        if request is in 'pending price review status ' => first review approved ,change request status to under negotiaion 
        if 'under negtiaion' : =>  customer approved the price , change status to 'waiting for first transfer'
        if 'waiting for accounting review' : => change to "pending for designs "
    """
    req = Quarter_service.objects.get(pk=id)
    if req.status == "pending price review":
        req.status = "under negotiaion"
        req.save()
    elif req.status == "under negotiaion":
        req.status = "waiting for first transfer"
        req.save()
        ## initiate transfer object ##
        transfer = Transfer(service=req, total_price=int(req.pricing.price))
        transfer.save()
        messages.success(
            request, 'تم اعتماد السعر .. سيتم البدء في التنفيذ بعد تحويل الجزء الاول من السعر')
    elif req.status == 'waiting for accounting review':
        req.status = "pending for designs "
        req.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def first_transfer(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        transfered = request.POST['transfered_ammount']
        files = request.FILES['files']
        notes = request.POST['notes']
        transfer = Transfer(transfer1_qty=int(transfered), service=req,
                            transfer1_file=files, transfer1_notes=notes, total_price=int(req.pricing.price))
        transfer.save()
        req.status = "waiting for accounting review"
        req.money_transfer = transfer
        req.save()
        messages.success(
            request, 'تم ارسال مستندات التحويل ')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
