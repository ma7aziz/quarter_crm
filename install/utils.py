from accounts.models import User
from service.models import Service_request
import datetime


def check_qouta(user_id):
    user = User.objects.get(pk=user_id)
    last_request = Service_request.objects.repair().filter(created_by=user).last()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    if last_request.timestamp.date == yesterday:
        user.current_requests = 0
