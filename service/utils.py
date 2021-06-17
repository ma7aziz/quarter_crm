from accounts.models import User
from service.models import Service_request
import datetime
import requests

def check_qouta(user_id):
    user = User.objects.get(pk=user_id)
    last_request = Service_request.objects.repair().filter(created_by=user).last()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    if last_request:
        if last_request.timestamp.date == yesterday:
            user.current_requests = 0

from .models import lateDays
def late_orders(service_type):
    late_days = lateDays.objects.get(pk = 1)
    orders = Service_request.objects.all().filter(
        service_type=service_type).filter(status="new").order_by('-timestamp')
    late = []
    for order in orders:
        days = order.timestamp.date() - datetime.datetime.today().date()
        
        if -days.days > late_days.days:
            late.append(order)
    return late

def send_new_request_message(req):
    message = f"تم تسجيل طلبك بنجاح \n رقم الطلب: #{req.request_number} \n "
    url =  f"https://mshastra.com/sendurlcomma.aspx?user=20099824&pwd=4nnnku&senderid=SMSAlert&mobileno={req.phone}&msgtext={message}&priority=High&CountryCode=+966"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)        


def send_appointment_message(req):
    if req.service_type == "install":
        message = f"تم تحديد موعد التركيب يوم {req.appointment.date}"
    elif req.service_type == "repair":
        message = f"تم تحديد موعد الصيانة يوم {req.appointment.date}"

    url = f"https://mshastra.com/sendurlcomma.aspx?user=20099824&pwd=4nnnku&senderid=SMSAlert&mobileno={req.phone}&msgtext={message}&priority=High&CountryCode=+966"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)