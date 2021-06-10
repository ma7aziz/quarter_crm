from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Service_request, Appointment, REQUEST_STATUS, Hold_reason
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .utils import check_qouta

# Create your views here.


def service_request_details(request, id):
    req = Service_request.objects.get(pk=id)
    technicians = User.objects.all().filter(role=8)
    appointment = Appointment.objects.all().filter(service_request=req).first()
    ctx = {
        'req': req,
        'tech': technicians,
        'appointment': appointment,
        'request_status': REQUEST_STATUS

    }

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
        service_request = Service_request.objects.get(
            pk=request.POST['request'])
        technician = User.objects.get(pk=request.POST['technician'])
        date = request.POST['appoint_date']
        appointment = Appointment(
            date=date, technician=technician, service_request=service_request, service_type=service_request.service_type)
        appointment.save()
        service_request.status = 'under_process'
        service_request.appointment = appointment
        service_request.save()
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
        if request.user.role == 1 or request.user.role == 2 or request.user.role == 3:
            if code == "0000" or code == repair_request.code:
                repair_request.status = "done"
                repair_request.save()
                appointment.status = "closed"
                appointment.save()
                messages.success(request, "تم تنفيذ الطلب ")
            else:
                # send error message
                messages.error(request, "برجاء ادخال كود صحيح ")
        else:
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
        repair_request = Service_request.objects.get(
            pk=request.POST['request_id'])
        repair_request.status = "closed"

        #  technician completed task count
        appointment = Appointment.objects.get(service_request=repair_request)
        technician = appointment.technician
        technician.completed_tasks += 1
        technician.save()

        # sales submitted orders count
        sales = repair_request.created_by
        sales.submitted_orders += 1
        sales.save()

        repair_request.save()

        messages.success(request, "تم تنفيذ و اغلاق الطلب بنجاح !")
    else:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_request(request, id):
    req = Service_request.objects.get(pk=id)
    req.delete()
    messages.success(request, "تم حذف الطلب ")
    if req.service_type == "repair":
        return redirect('/repair')
    elif req.service_type == "install":
        return redirect('/install')
    elif request.user.role == 1:
        return redirect('dashboard')


def hold(request, id):
    if request.method == "POST":
        req = Service_request.objects.get(pk=request.POST['req_id'])
        reason = request.POST['hold_reason']
        if req.hold_reason:
            req.hold_reason.reason = reason
            req.hold_by = request.user
            if request.FILES["holding_file"]:
                req.hold_reason.file = request.FILES["holding_file"]

            req.hold_reason.save()
            req.hold = True
            req.save()
            messages.success(request, "تم تعليق الطلب !")

        else:
            hold_reason = Hold_reason(
                service=req, reason=reason, hold_by=request.user)
            if request.FILES["holding_file"]:
                hold_reason.file = request.FILES["holding_file"]
            hold_reason.save()
            req.hold_reason = hold_reason
            req.hold = True
            req.save()
            messages.success(request, "تم تعليق الطلب !")
    else:
        req = Service_request.objects.get(pk=id)
        req.hold = False
        req.save()
        messages.success(request, "تم اعادة تفعيل الطلب  !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_status(request):
    if request.method == "POST":
        req = Service_request.objects.get(pk=request.POST['request'])
        req.status = request.POST['new_status']
        req.save()
        messages.success(request, "تم تحديث حالة الطلب بنجاح !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deactivate_request(request, id):
    req = Service_request.objects.get(pk=id)
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
def multiple_delete(request):
    if request.is_ajax:
        ids = request.POST.getlist('ids[]')
        for i in ids:
            req = Service_request.objects.get(pk=i)
            req.delete()
        data = {
            'message':  'تم حذف الطلبات المختارة '
        }

        return JsonResponse(data)


def favorite(request, id):
    """
    ALLOW USER TO ADD REQUEST TO FAVORITES 
    """
    req = Service_request.objects.get(pk=id)
    user = request.user
    if not req.favourite:
        print("favorite")
        check_qouta(request.user.id)
        if user.favourite_qouta.current_requests < user.favourite_qouta.max_requests:
            service = req
            service.favourite = True
            service.save()
            user.favourite_qouta.current_requests += 1
            user.favourite_qouta.save()
            messages.success(request, "تم الاضافة للمفضلات ")
        else:
            messages.error(request, "لم يتم أضافة الطلب الي المفضلات ")
    else:  # remove from favorites
        service = req
        service.favourite = False
        service.save()
        user.favourite_qouta.current_requests -= 1
        user.favourite_qouta.save()
        messages.success(request, "تم الحذف من المفضلات ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
