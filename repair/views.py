from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import RepairRequestForm
from .models import Repair_request, Appointment
from accounts.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def repair_index(request):
    requests = Repair_request.objects.all().filter(created_by=request.user)
    ctx = {
        "form": RepairRequestForm,
        "requests": requests
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
        print(repair_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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

    return redirect('/')


def complete_request(request):
    """
    change request status from under process to done .. using a verification code .
    """
    if request.method == "POST":
        repair_request = Repair_request.objects.get(
            pk=request.POST['request_id'])
        print(repair_request.code)
        code = request.POST['code']
        if code == repair_request.code:
            repair_request.status = "done"
            repair_request.save()

        else:
            # send error message
            pass

    return redirect('/')


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

        return redirect('/')


def change_status(request):
    pass
    # TODO
