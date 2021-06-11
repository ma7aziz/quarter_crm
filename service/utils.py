from accounts.models import User
from service.models import Service_request
import datetime


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
        if days.days <= -int(late_days.days):
            late.append(order)
    return late
