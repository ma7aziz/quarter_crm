from django.shortcuts import render, redirect

from .forms import RepairRequestForm
from .models import Repair_request, Appointment
from accounts.models import User
# Create your views here.


def repair_request(request):
    if request.method == 'POST':
        print(request.POST)
        form = RepairRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')


def repair_appointment(request):
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
