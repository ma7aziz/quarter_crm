from django.template.loader import render_to_string
from .forms import QuarterForm
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from .models import Price, Quarter_service, Transfer, Design, Purchase , ExcutionFiles , Excution
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
        user = request.user
        new_request = Quarter_service(
            name=name, phone=phone, location=location, email=email, notes=notes, created_by=request.user)
        new_request.customer = add_customer(phone, name, email)
        new_request.save()
        user.submitted_orders += 1
        user.save()
        if request.FILES:
            new_request.file = request.FILES['attach_file']
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

    return redirect('index')


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
        """
            create new pricing object 
        """
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
            if request.user == req.pricing.created_by or request.user.role == 7 or request.user.role == 1 or request.user.role == 4 :
                req.pricing.price = price
                req.pricing.files = files
                req.pricing.notes = notes
                if req.pricing.status == "rejected":
                    if request.user.role == 1 or request.user.role == 7 or request.user.role == 4:
                        req.pricing.status = "pending"
                        req.pricing.save()
                        req.status == 4
                        req.save()
                else:
                    req.status == 3
                req.pricing.save()
                req.save()
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
        req.pricing.status == "approved"
        req.pricing.save()
        ## initiate transfer object ##
        transfer = Transfer(service=req)
        transfer.save()
        if req.pricing.price:
            transfer.total_price = int(req.pricing.price)
            transfer.save()
            
        messages.success(
            request, ' تم اعتماد السعر .. سيتم البدء في التنفيذ بعد تحويل الجزء الاول من السعر المتفق عليه ')
    elif req.status == 6: 
        req.status = 7
        req.save()
 #confirm designs => purchase 
    elif req.status == 8:
        req.status = 14
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
        transfer = Transfer.objects.get_or_create(service=req)
        # transfer = Transfer(transfer1_qty=int(transfered), service=req,
        #                     transfer1_file=files, transfer1_notes=notes, total_price=int(req.pricing.price))
        t = transfer[0]
        t.transfer1_qty = int(transfered)
        t.transfer1_file = files
        t.transfer1_notes = notes
        if request.POST.get("total_price"):
            t.total_price = int(request.POST['total_price'])
        t.save()
        req.status = 6
        req.money_transfer = t
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
        design = Design.objects.get_or_create(service=req)
        d = design[0]
        d.files = request.FILES['files']
        d.notes = request.POST['notes']
        d.save()
        req.designs = d
        req.status = 8
        req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def attach_purchase(request):
    if request.method == "POST":
        req = Quarter_service.objects.get(pk=request.POST['request'])
        files = request.FILES['files']
        notes = request.POST['notes']
        if req.purchase:
            req.purchase.files = files 
            req.purchase.notes = notes
            req.purchase.created_by = request.user
            req.purchase.save()
        else:
            purchase = Purchase(service=req, files=files,
                                notes=notes, created_by=request.user)
            purchase.save()
            req.purchase = purchase
        req.status = 9 
        req.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def end_request(request, id):
    req = Quarter_service.objects.get(pk=id)
    req.status = 15
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


def edit_request(request):
    if request.method == "POST":
        req = get_object_or_404(Quarter_service, pk=request.POST['req'])
        if request.POST.get('name'):
            req.name = request.POST['name']

        elif request.POST.get('phone'):
            req.phone = request.POST['phone']
        elif request.POST.get('email'):
            req.email = request.POST['email']
        elif request.POST.get('location'):
            req.location = request.POST['location']

        req.save()
        messages.success(
            request, 'تم التعديل!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def attach_excution_files(request):
    req = Quarter_service.objects.get(pk = request.POST['request'] )
    excution = Excution(service = req , notes = request.POST['notes'])
    excution.save() 
    if req.status == 9 :  ### first excution 
        req.first_excution = excution
        req.status = 10
        req.save()
        excution.name = f"first excution - {req.id} "
        excution.save()
    elif req.status == 12 :
        req.second_excution = excution
        req.status =13
        req.save()
        excution.name = f"second excution - {req.id} "
        excution.save()

    for f in request.FILES.getlist("files"):
        file = ExcutionFiles(
            excution = excution , file = f 
        )
        file.save()
        excution.files.add(file)
        excution.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))