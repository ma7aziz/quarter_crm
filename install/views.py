from django.http import JsonResponse
from django.core import serializers
from service.utils import check_qouta, late_orders, new_req_msg
import datetime
from django.shortcuts import render
from service.models import Service_request, Appointment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from core.add_customer import add_customer
# Create your views here.


@login_required()
def index(request):
    check_qouta(request.user.id)
    if request.user.role == 4:
        requests = Service_request.objects.install().filter(
            created_by=request.user).order_by('-timestamp', '-favourite')

    elif request.user.role == 1 or request.user.role == 2:
        if request.GET.get('status'):
            if request.GET.get('status') == "all":
                requests = Service_request.objects.install().order_by('-favourite', '-timestamp')
            else:
                requests = Service_request.objects.install().order_by(
                    '-favourite', '-timestamp').filter(status=request.GET['status'])
        else:
            requests = Service_request.objects.all().filter(
                service_type="install").order_by('-favourite', '-timestamp')
            # requests = Service_request.objects.install().order_by('-favourite', '-timestamp')
    elif request.user.role == 3:
        requests = Appointment.objects.filter(
            status="open", technician=request.user)
    appointments = Appointment.objects.install().filter(
        status="open").order_by('date')

    ctx = {
        "requests": requests,
        "on_hold": Service_request.objects.on_hold().filter(service_type="install"),
        "new_requests": requests.filter(status="new"),
        "favorites": Service_request.objects.install_favourites(),
        "appointments": appointments,
        "late_orders": late_orders("install"),
        "need_confirm": Service_request.objects.done().filter(service_type="install"),
        "current_requests": Service_request.objects.install().exclude(status="new"),
    }
    return render(request, 'repair/index.html', ctx)


@login_required
def install_request(request):
    """
    initiate service request  === done by sales team
    """
    if request.method == 'POST':

        customer_name = request.POST['customername']
        phone = request.POST['phone']
        address = request.POST['address']

        customer_type = "cash"
        invoice_number = request.POST['invoice_number']
        user = request.user
        install_request = Service_request(service_type="install", created_by=user, customer_name=customer_name, phone=phone,
                                          invoice_number=invoice_number,
                                          address=address, customer_type=customer_type, notes=request.POST['notes'])
        install_request.customer = add_customer(phone, customer_name)
        install_request.save()

        if request.FILES:
            install_request.file = request.FILES['attach_file']
            install_request.save()
            user.submitted_orders += 1
            user.save()

        install_request.request_number = 'inst{id}'.format(
            id=install_request.id)
        install_request.save()
        check_qouta(request.user.id)
        if "checked" in request.POST.getlist('favorite'):
            if user.favourite_qouta.current_requests < user.favourite_qouta.max_requests:
                service = install_request
                service.favourite = True
                service.save()
                user.favourite_qouta.current_requests += 1
                user.favourite_qouta.save()
                messages.success(request, "تم التسجيل و الاضافة للمفضلات ")
            else:
                messages.success(request, "لم يتم أضافة الطلب الي المفضلات ")
        else:
            messages.success(request, "تم تسجيل طلبك بنجاح")
        new_req_msg(install_request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_order_list(request):
    if request.is_ajax():
        status = request.GET.get("status")
        requests = Service_request.objects.all().filter(status=status)
        data = serializers.serialize("json", requests)
        return JsonResponse(data, safe=False)
