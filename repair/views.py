from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render


from service.models import Appointment, Service_request

# Create your views here.


@login_required
def repair_index(request):
    print(request.user.role)
    if request.user.role == 4:

        requests = Service_request.objects.repair().filter(
            created_by=request.user).order_by('-timestamp')
    elif request.user.role == 1 or request.user.role == 2:

        requests = Service_request.objects.repair().order_by('-timestamp')
    elif request.user.role == 3:
        requests = Appointment.objects.filter(
            status="open", technician=request.user)

    ctx = {
        "requests": requests,
        "need_confirm": Service_request.objects.done().filter(service_type="repair")
    }
    return render(request, 'repair/index.html ', ctx)


@login_required
def repair_request(request):
    """
    initiate service request  === done by sales team 
    """
    if request.method == 'POST':
        customer_name = request.POST['customername']
        phone = request.POST['phone']
        address = request.POST['address']
        machine_type = request.POST['machine_type']
        customer_type = request.POST['customer_type']
        invoice_number = request.POST['invoice_number']
        user = request.user
        repair_request = Servrequests = Service_request(service_type="repair", created_by=user, customer_name=customer_name, phone=phone,
                                                        machine_type=machine_type, invoice_number=invoice_number,
                                                        address=address, customer_type=customer_type, notes=request.POST['notes'], file=request.FILES['attach_file'])
        repair_request.save()
        messages.success(request, "تم تسجيل طلبك بنجاح")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_status(request):
    pass
    # TODO