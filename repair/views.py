from email import message
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render , get_object_or_404
from core.add_customer import add_customer
from service.utils import check_qouta, late_orders, new_req_msg
from service.models import Appointment, Service_request , RequestFile
from . models import SparePartRequst , SparePartsRequestFile
from django.core.exceptions import PermissionDenied

# Create your views here.


@login_required
def repair_index(request):
    check_qouta(request.user.id)
    on_hold = []
    if request.user.role == 4:
        requests = Service_request.objects.repair().filter(
            created_by=request.user).order_by('-timestamp')
    elif request.user.role == 1 or request.user.role == 3:
        if request.GET.get('status'):
            if request.GET.get('status') == "all":
                requests = Service_request.objects.repair().order_by('-favourite', '-timestamp')
            else:
                requests = Service_request.objects.repair().order_by(
                    '-favourite', '-timestamp').filter(status=request.GET['status'])
        else:
            requests = Service_request.objects.all().filter(
                service_type="repair").order_by('-favourite', '-timestamp')
        on_hold = Service_request.objects.on_hold().filter(service_type="repair")
    elif request.user.role == 3:
        requests = Appointment.objects.filter(
            status="open", technician=request.user)
    appointments = Appointment.objects.repair().filter(
        status="open").order_by("date")
    spare_parts_request = SparePartRequst.objects.all().order_by("-status").order_by("-timestamp")
    ctx = {
        "new_requests": Service_request.objects.repair().filter(status="new").order_by("-timestamp"),
        "current_requests": Service_request.objects.repair().filter(status="under_process"),
        "requests": requests,
        "need_confirm": Service_request.objects.done().filter(service_type="repair"),
        'on_hold': on_hold,
        "appointments": appointments,
        "late_orders": late_orders("repair"), 
        "finished_requests": Service_request.objects.repair().exclude(status="new").exclude(status="under_process"),
        "open_spare_parts_requests":spare_parts_request.filter(status = "open"),
        "spare_parts_requests":spare_parts_request
    }
    return render(request, 'repair/index.html', ctx)


@login_required
def repair_request(request):
    """
    initiate service request
    """
    if request.method == 'POST':
        print(request.POST)
        customer_name = request.POST['customername']
        phone = request.POST['phone']
        address = request.POST['address']
        machine_type = request.POST['machine_type']
        customer_type = request.POST['customer_type']
        invoice_number = request.POST['invoice_number']
        user = request.user
        if customer_type == "warranty" and invoice_number == "":
            messages.error(
                request, "يجب ادخال رقم الفاتورة لتسجيل عميل الضمان ")
        else:
            repair_request = Service_request(service_type="repair", created_by=user, customer_name=customer_name, phone=phone,
                                             machine_type=machine_type, invoice_number=invoice_number,
                                             address=address, customer_type=customer_type, notes=request.POST['notes'])
            repair_request.customer = add_customer(phone, customer_name)
            repair_request.save()

            if request.FILES.getlist('attach_file'):
                for f in request.FILES.getlist("attach_file"):
                    new_file = RequestFile(service=repair_request, file=f)
                    new_file.save()
                    repair_request.request_files.add(new_file)
                    repair_request.save()
            user.submitted_orders += 1
            user.save()
            repair_request.request_number = 'rep{id}'.format(
                id=repair_request.id)
            repair_request.save()
            if "company" in request.POST:
                company = User.objects.get(pk = request.POST["company"])
                repair_request.company = company
                repair_request.save()
            check_qouta(request.user.id)
            if "checked" in request.POST.getlist('favorite'):
                if user.favourite_qouta.current_requests < user.favourite_qouta.max_requests:
                    service = repair_request
                    service.favourite = True
                    service.save()
                    user.favourite_qouta.current_requests += 1
                    user.favourite_qouta.save()
                else:
                    messages.success(
                        request, "لم يتم أضافة الطلب الي المفضلات ")
            messages.success(request, "تم تسجيل طلبك بنجاح")
            new_req_msg(repair_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def spare_request(request):
    if request.method == "POST":
        service_request =Service_request.objects.get(pk = request.POST["service"]) 
        part_name = request.POST["part_name"]
        details = request.POST["details"]
        
        spare_part_request = SparePartRequst(service_request = service_request , 
                            part_name = part_name , details = details , 
                            company = service_request.company , created_by = request.user )
        spare_part_request.save()
        service_request.spare_part_request.add(spare_part_request)
        service_request.save()
        if request.FILES.getlist("attach_file"):
            for f in request.FILES.getlist("attach_file"):
                file = SparePartsRequestFile(request = spare_part_request , file = f)
                file.save()
                spare_part_request.files.add(file)
                spare_part_request.save()
        messages.success(request , "تم تسجيل الطلب")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def spare_request_details(request , id ):
    spare_request = get_object_or_404(SparePartRequst , pk= id)
    return render(request , "repair/spare_request_details.html" , {"req":spare_request})


def change_spare_request_status(request , id):
    if request.user.role == 1 or request.user.role == 2:
        spare_request = get_object_or_404(SparePartRequst , pk=id )
        if spare_request.status == "open":
            spare_request.status = "closed" 
            spare_request.save()
            messages.success(request , "تم اغلاق الطلب ")
        else:
            spare_request.status = "open"
            spare_request.save()
            messages.success(request , "تم اعادة تفعيل الطلب ")
        
    else:
        messages.error(request , "عفوا .. لايمكنك اجراء هذه العملية !!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def delete_spare_request(request , id):
    if request.user.role == 1 or request.user.role == 2:
       spare_request = get_object_or_404(SparePartRequst , pk=id )
       spare_request.delete() 
    else:
        messages.error(request , "عفوا .. لايمكنك اجراء هذه العملية !!")
    return redirect(f"/service_request_detils/{spare_request.service_request.id}")