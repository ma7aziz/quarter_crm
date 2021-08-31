import csv
import io
from itertools import chain
from operator import attrgetter

import xlwt
from accounts.models import User
from core.models import Customer
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
# importing get_template from loader
from django.template.loader import get_template
from django.views.generic import View
from quarter.models import Quarter_service
from service.models import Service_request

from .resources import UsersResource
# import render_to_pdf from util.py
from .utils import render_to_pdf

# Create your views here.


def export_users_csv(request):
    """
        Export all website users data
    """
    response = HttpResponse(content_type='text/csv , charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    response.write(u'\ufeff'.encode('utf8'))
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
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="current_install/repair_requests.xls"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["id", "service_type", "customer_name", "customer_type", "phone",
                     "address", "time_created", "status", "created by"])

    processes = Service_request.objects.all().exclude(status="new").values_list("id", "service_type", "customer_name", "customer_type", "phone",
                                                                                "address", "timestamp__date", "status", "created_by__username")

    for process in processes:
        writer.writerow(process)

    return response


def export_all_services(request):
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="all_install/repair_requests.xls"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["id", "service_type", "customer_name", "customer_type", "phone",
                     "address", "time_created", "status", "created by"])

    processes = Service_request.objects.all().values_list("id", "service_type", "customer_name", "customer_type", "phone",
                                                                                "address", "timestamp__date", "status", "created_by__username")

    for process in processes:
        writer.writerow(process)

    return response


def export_all_quarter_services(request):
    """
        Export current quarter proceses
    """
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="current_quarter_services.xls"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["id",  "customer_name", "phone",
                     "address", "time_created", "created_by",  "status", "price", "outstanding_ammount"])

    processes = Quarter_service.objects.all().values_list("id", "name", "phone",
                                                          "location", "timestamp__date", "created_by__name",  "status", "pricing__price", "transfer__outstanding_ammount")

    for process in processes:
        writer.writerow(process)

    return response


def export_current_quarter_services(request):
    """
        Export current quarter proceses
    """
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="current_quarter_services.xls"'
    response.write(u'\ufeff'.encode('utf8'))
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
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="customer_data.xls"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["name", "phone", ])

    processes = Customer.objects.all().values_list("name", "phone",)

    for process in processes:
        writer.writerow(process)

    return response


def export_repair_customers(request):
    response = HttpResponse(content_type='text/csv, charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="repair_customer_data.xls"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(["الاسم", "الهاتف"])

    processes = Service_request.objects.repair(
    ).values_list("customer_name", "phone", )

    for process in processes:
        writer.writerow(process)

    return response


def print_invoice(request):
    pdf = render_to_pdf('pdf_reports/invoice.html')
    return HttpResponse(pdf, content_type='application/pdf')
