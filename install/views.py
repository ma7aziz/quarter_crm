from django.shortcuts import render
from service.models import Service_request, Appointment
# Create your views here.


def index(request):
    if request.user.role == 4:

        requests = Service_request.objects.all().filter(created_by=request.user)
    elif request.user.role == 1 or request.user.role == 2:

        requests = Service_request.objects.all().order_by('-timestamp')
    elif request.user.role == 3:

        requests = Appointment.objects.filter(
            status="open", technician=request.user)
        print(requests, request.user.role)
    ctx = {
        "requests": requests,
        "need_confirm": Service_request.objects.done().filter(service_type="repair")
    }
    return render(request, 'repair/index.html ', ctx)
