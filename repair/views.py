from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import RepairRequestForm
from .models import Appointment, Repair_request

# Create your views here.


@login_required
def repair_index(request):
    if request.user.role == 4:

        requests = Repair_request.objects.all().filter(created_by=request.user)
    elif request.user.role == 1 or request.user.role == 2:

        requests = Repair_request.objects.all().order_by('-timestamp')
    elif request.user.role == 3:

        requests = Appointment.objects.filter(
            status="open")
        print(requests, request.user.role)
    ctx = {
        "requests": requests,
        "need_confirm": Repair_request.objects.done()
    }
    return render(request, 'repair/index.html ', ctx)


@login_required
def repair_request(request):
    """
    initiate service request  === done by sales team 
    """
    if request.method == 'POST':
        # print(request.FILES['attach_file'])
        customer_name = request.POST['customername']
        phone = request.POST['phone']
        address = request.POST['address']
        machine_type = request.POST['machine_type']
        customer_type = request.POST['customer_type']
        invoice_number = request.POST['invoice_number']
        user = request.user
        repair_request = Repair_request(created_by=user, customer_name=customer_name, phone=phone,
                                        machine_type=machine_type, invoice_number=invoice_number, address=address, customer_type=customer_type, notes=request.POST['notes'])
        repair_request.save()
        messages.success(request, "تم تسجيل طلبك بنجاح")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def repair_request_details(request, id):
    req = Repair_request.objects.get(pk=id)
    technicians = User.objects.all().filter(role=3)
    appointment = Appointment.objects.all().filter(repair_request=req).first()
    ctx = {
        'req': req,
        'tech': technicians,
        'appointment': appointment


    }
    return render(request, 'repair/request_details.html', ctx)


def appointment_details(request, id):
    appointment = Appointment.objects.get(pk=id)
    ctx = {
        "appointment": appointment
    }
    print(appointment.repair_request.code)
    return render(request, 'repair/appointment_details.html', ctx)


def repair_appointment(request):
    """
    set appointment && asign technician for repair service 
    - should be done by admin or supervisor 
    - send message to client 
    - change request status from new => underprocess 

    """
    if request.method == 'POST':
        repair_request = Repair_request.objects.get(pk=request.POST['request'])
        technician = User.objects.get(pk=request.POST['technician'])
        date = request.POST['appoint_date']
        appointment = Appointment(
            date=date, technician=technician, repair_request=repair_request)
        appointment.save()
        repair_request.status = 'under_process'
        repair_request.save()
        messages.success(request, "تم تحديد الموعد !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_request(request):
    """
    change request status from under process to done .. using a verification code .
    """
    if request.method == "POST":
        repair_request = Repair_request.objects.get(
            pk=request.POST['request_id'])
        appointment = Appointment.objects.get(pk=request.POST['appoint_id'])
        code = request.POST['code']
        if code == repair_request.code:
            repair_request.status = "done"
            repair_request.save()
            appointment.status = "closed"
            appointment.save()
            messages.success(request, "تم تنفيذ الطلب ")
        else:
            # send error message
            messages.error(request, "برجاء ادخال كود صحيح ")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def close_request(request):
    """
      done by supervisor or admin 
      confirm finishing the repair service and close the request 
      == change status to closed  
    """
    if request.method == "POST":
        repair_request = Repair_request.objects.get(
            pk=request.POST['request_id'])
        repair_request.status = "closed"
        repair_request.save()
        messages.success(request, "تم تنفيذ و اغلاق الطلب بنجاح !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_status(request):
    pass
    # TODO
