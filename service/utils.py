from accounts.models import User
from service.models import Service_request
import datetime
import requests
from .models import lateDays

import json


def check_qouta(user_id):
    user = User.objects.get(pk=user_id)
    last_request = Service_request.objects.all().filter(
        created_by=user).filter(favourite=True).last()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    if last_request:
        if last_request.timestamp.date() < today:
            user.favourite_qouta.current_requests = 0
            user.favourite_qouta.save()
    else:
        user.favourite_qouta.current_requests = 0
        user.favourite_qouta.save()


def late_orders(service_type):
    late_days = lateDays.objects.get(pk=1)
    orders = Service_request.objects.all().filter(
        service_type=service_type).filter(status="new").order_by('-timestamp')
    late = []
    for order in orders:
        days = order.timestamp.date() - datetime.datetime.today().date()

        if -days.days > late_days.days:
            late.append(order)
    return late

# def send_new_request_message(req):
#     message = f"تم تسجيل طلبك بنجاح \n رقم الطلب: #{req.request_number}\n"
#     url =  f"https://mshastra.com/sendurlcomma.aspx?user=20099824&pwd=4nnnku&senderid=SMSAlert&mobileno={req.phone}&msgtext={message}&priority=High&CountryCode=+966"
#     print(url)
#     payload={}
#     headers = {}
#     response = requests.request("GET", url, headers=headers, data=payload)


def new_req_msg(req):
    msg = "تم تسجيل طلبك بنجاح"
    url = f"https://mshastra.com/sendurlcomma.aspx?user=20099824&pwd=4nnnku&senderid=SMSAlert&mobileno={req.phone}&msgtext={msg}&priority=High&CountryCode=+966"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)


def send_appointment_message(req):
    if req.service_type == "install":
        message = f"تم تحديد موعد التركيب يوم {req.appointment.date}"
    elif req.service_type == "repair":
        message = f"تم تحديد موعد الصيانة يوم {req.appointment.date}"

    url = f"https://mshastra.com/sendurlcomma.aspx?user=20099824&pwd=4nnnku&senderid=SMSAlert&mobileno={req.phone}&msgtext={message}&priority=High&CountryCode=+966"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)


def get_data():
    pass
    # response = requests.get('http://localhost:8000/api/requests')
    # data = response.json()
    # for r in data:
    #     print(r["id"], r['time'])


def set_archived():
    orders = Service_request.objects.all().exclude(archived=True).exclude(status="new").exclude(
        status="under_process").exclude(hold=True).order_by('-timestamp')
    for order in orders:
        days = order.timestamp.date() - datetime.datetime.today().date()
        if -days.days > 30:
            order.archived = True
            order.save()
