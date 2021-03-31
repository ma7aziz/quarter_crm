from django.shortcuts import render
from .models import Service_request, Appointment
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.


def service_request_details(request, id):
    req = Service_request.objects.get(pk=id)
    technicians = User.objects.all().filter(role=3)
    appointment = Appointment.objects.all().filter(service_request=req).first()
    ctx = {
        'req': req,
        'tech': technicians,
        'appointment': appointment


    }
    print(request.user.role, req.status)
    return render(request, 'repair/request_details.html', ctx)


def appointment_details(request, id):
    appointment = Appointment.objects.get(pk=id)
    ctx = {
        "appointment": appointment
    }
    print(appointment.service_request.code)
    return render(request, 'repair/appointment_details.html', ctx)


def service_appointment(request):
    """
    set NEW appointment && asign technician for repair service 
    - should be done by admin or supervisor 
    - send message to client 
    - change request status from new => underprocess 

    """
    if request.method == 'POST':
        repair_request = Servrequests = Service_request.objects.get(
            pk=request.POST['request'])
        technician = User.objects.get(pk=request.POST['technician'])
        date = request.POST['appoint_date']
        appointment = Appointment(
            date=date, technician=technician, service_request=repair_request)
        appointment.save()
        repair_request.status = 'under_process'
        repair_request.save()
        messages.success(request, "تم تحديد الموعد !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_appointment(request):
    appointment = Appointment.objects.get(pk=request.POST["appoint_id"])
    technician = User.objects.get(pk=request.POST['technician'])
    date = request.POST['appoint_date']
    appointment.technician = technician
    appointment.date = date
    appointment.save()
    messages.success(request, "تم تغيير الموعد !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def complete_request(request):
    """
    change request status from under process to done .. using a verification code .
    """
    if request.method == "POST":
        repair_request = Service_request.objects.get(
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
        repair_request = Servrequests = Service_request.objects.get(
            pk=request.POST['request_id'])
        repair_request.status = "closed"
        repair_request.save()
        messages.success(request, "تم تنفيذ و اغلاق الطلب بنجاح !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
