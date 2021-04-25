import xlwt
from django.contrib.auth.models import User
from accounts.models import User
import csv
from django.shortcuts import render
from django.http import HttpResponse
from .resources import UsersResource
from operator import attrgetter
from itertools import chain
from service.models import Service_request
from quarter.models import Quarter_service
from core.models import Customer
# Create your views here.


def export_users_csv(request):
    """
        Export all website users data
    """
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    writer = csv.writer(response)
    writer.writerow(['id', 'username',  'name', 'phone', 'email', 'role', 'last_login',
                     'completed_tasks', 'submitted_orders'])

    users = User.objects.all().values_list(
        'id', 'username',  'name', 'phone', 'email', 'role', 'last_login',
        'completed_tasks', 'submitted_orders')
    for user in users:
        writer.writerow(user)

    return response


def export_current_service(request):
    """
        Export Repair / Install Current Processes
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="current_install_requests.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "service_type", "customer_name", "customer_type", "phone",
                    "address", "time_created", "status", "created by"])

    processes = Service_request.objects.all().exclude(status="new").values_list("id", "service_type", "customer_name", "customer_type", "phone",
                                                                                "address", "timestamp__date", "status", "created_by")

    for process in processes:
        writer.writerow(process)

    return response


def export_current_quarter_services(request):
    """
        Export current quarter proceses
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="current_quarter_services.csv"'

    writer = csv.writer(response)
    writer.writerow(["id",  "customer_name", "phone",
                    "address", "time_created", "created_by",  "status", "price", "outstanding_ammount"])

    processes = Quarter_service.objects.all().exclude(status=1).values_list("id", "name", "phone",
                                                                            "location", "timestamp__date", "created_by__name",  "status", "pricing__price", "transfer__outstanding_ammount")

    for process in processes:
        writer.writerow(process)

    return response


def export_customers_data(request):
    """
        Export customer data 
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_data.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "name", "phone", "email", ])

    processes = Customer.objects.all().values_list("id", "name", "phone", "email")

    for process in processes:
        writer.writerow(process)

    return response
