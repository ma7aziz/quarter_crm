from service.models import Service
from datetime import timedelta
from django.utils import timezone


def check_old_requests():
    print('check_old_requests ')
    services = Service.objects.all().filter(
        status = 'closed',
        created_at__lte = timezone.now()-timedelta(days=30)
    )
    for service in services :
        service.archive = True
        service.save()
        