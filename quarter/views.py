from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Price, Quarter_service, Transfer, Design, Purchase
from core.add_customer import add_customer
from .choices import STATUS_CHOICES
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@login_required
def index(request):
    if request.GET.get("status"):
        if request.GET.get("status") == "0":
            all_requests = Quarter_service.objects.all().order_by('-timestamp')
        else:
            all_requests = Quarter_service.objects.all().order_by(
                '-timestamp').filter(status=request.GET.get("status"))
    else:
        all_requests = Quarter_service.objects.all().order_by('-timestamp')
    ctx = {
        "money_transfers": Transfer.objects.all(),
        # "new_transfers": Quarter_service.objects.filter(status=6),
        "all_requests": all_requests,
        "new_requests": Quarter_service.objects.all().filter(status=1).order_by('-timestamp'),
        "pricing": Quarter_service.objects.all().filter(status=3),
        "design": Quarter_service.objects.all().filter(status=8),
        "status_choices": STATUS_CHOICES
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
        new_request.customer = add_customer(phone, name, email)
        new_request.save()
        messages.success(request, "تم تسجيل طلبك بنجاح")
        new_request.request_number = "qua{id}".format(id=new_request.id)
        new_request.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def request_details(request, id):
    req = Quarter_service.objects.get(pk=id)
    return render(request, 'quarter/request_details.html', {'req': req, 'status_choices': STATUS_CHOICES})


def delete_request(request, id):
    req = Quarter_service.objects.get(pk=id)
    req.delete()
    messages.success(request, "تم حذف الطلب ")
    return redirect('quarter_index')


def hold_request(request, id):
    req = Quarter_service.objects.get(pk=id)
    req.hold = not req.hold
    req.save()
    if req.hold:
        messages.success(request, "تم تعليق الطلب !")
    else:
        messages.success(request, "تم اعادة تفعيل الطلب  !")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_status(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        req.status = request.POST['new_status']
        req.save()
        messages.success(request, "تم تحديث حالة الطلب بنجاح !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deactivate_request(request, id):
    req = Quarter_service.objects.get(pk=id)
    req.active = not req.active
    req.save()
    if req.active:
        if req.hold:
            req.hold = False
            req.save()
        messages.success(request, "تم اعادة تفعيل الطلب  !")
    else:
        messages.success(request, "تم اغلاق الطلب  !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def quarter_multi_delete(request):
    if request.is_ajax:
        ids = request.POST.getlist('ids[]')
    for i in ids:
        req = Quarter_service.objects.get(pk=i)
        req.delete()
    data = {
        'message':  'تم حذف الطلبات المختارة '
    }

    return JsonResponse(data)


def pricing(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        price = request.POST['price']
        files = request.FILES['files']
        notes = request.POST['notes']
        if not req.pricing:
            # CREATE NEW PRICING OBJECT
            price = Price(service=req, price=price, files=files,
                          notes=notes, created_by=request.user)
            price.save()
            req.pricing = price
            req.status = 3
            req.save()
            messages.success(request, "تم ارسال السعر .")
        else:
            # EDIT PRICE BY THE SAME PRICING USER
            if request.user == req.pricing.created_by or request.user.role == 7:
                req.pricing.price = price
                req.pricing.files = files
                req.pricing.notes = notes
                req.pricing.save()
                messages.success(request, "تم تعديل السعر .. ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirm_process(request, id):
    """
        if request is in 'pending price review status ' => first review approved ,change request status to under negotiaion 
        if 'under negtiaion' : =>  customer approved the price , change status to 'waiting for first transfer'
        if 'waiting for accounting review' : => change to "pending for designs "
        if 'Pending Designs approval'  : => "Excution"
    """
    req = Quarter_service.objects.get(pk=id)
    if req.status == 3:
        req.status = 4
        req.save()
    elif req.status == 4:
        req.status = 5
        req.save()
        ## initiate transfer object ##
        transfer = Transfer(service=req, total_price=int(req.pricing.price))
        transfer.save()
        messages.success(
            request, ' تم اعتماد السعر .. سيتم البدء في التنفيذ بعد تحويل الجزء الاول من السعر المتفق عليه ')
    elif req.status == 6:
        req.status = 7
        req.save()
    elif req.status == 8:
        req.status = 9
        req.save()
    elif req.status == 11:
        req.status = 12
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
        req.status = 6
        req.money_transfer = transfer
        req.save()
        messages.success(
            request, 'تم ارسال مستندات التحويل ')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def second_transfer(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        files = request.FILES['files']
        notes = request.POST['notes']
        transfered = request.POST['transfered_ammount']

        transfer = Transfer.objects.all().filter(service=req).first()
        transfer.transfer2_qty = int(transfered)
        transfer.transfer2_file = files
        transfer.transfer2_date = datetime.now()
        transfer.transfer2_notes = notes

        transfer.save()
        req.status = 11
        req.save()
        messages.success(
            request, 'تم ارسال مستندات التحويل ')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def attach_designs(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        files = request.FILES['files']
        notes = request.POST['notes']
        design = Design(service=req, files=files, notes=notes)
        design.save()
        req.designs = design
        req.status = 8
        req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def attach_purchase(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        files = request.FILES['files']
        notes = request.POST['notes']
        purchase = Purchase(service=req, files=files,
                            notes=notes, created_by=request.user)
        purchase.save()
        req.purchase = purchase
        req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def end_request(request, id):
    req = Quarter_service.objects.get(pk=id)
    req.status = 13
    req.save()
    messages.success(
        request, 'اتمام الخدمة بنجاح  ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reject_price(request):
    req = Quarter_service.objects.get(pk=request.POST['req_id'])
    req.pricing.status = "rejected"
    if request.POST['proposed_price']:
        req.pricing.proposed_price = request.POST['proposed_price']
    if request.POST['rejection_notes']:
        req.pricing.rejection_notes = request.POST['rejection_notes']
    req.pricing.save()
    req.status = 3
    req.save()
    messages.success(
        request, 'تم ارسال الملاحظات للادارة !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
