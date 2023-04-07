from datetime import datetime, timedelta

from django.db.models import Count, DateField, Max, Q ,Sum
from django.db.models.functions import Cast
from django.utils import timezone

from core.models import LateDays

from . import models


def generate_ref_number(service_type):

    prefix = 'N' if service_type == 'install' else 'R'
    year = str(datetime.now().year)[-2:]

    last_ref_number = models.Service.objects.filter(
        ref_number__startswith=f'{prefix}{year}'
    ).aggregate(Max('ref_number'))['ref_number__max']

    if not last_ref_number:
        return f'{prefix}{year}001'

    last_number = int(last_ref_number[-3:])
    new_number = f'{last_number+1:03d}'
    return f'{prefix}{year}{new_number}'


def get_late_count(service):

    days = LateDays.objects.last().days
    threshold_date = timezone.now() - timedelta(days=days - 1)
    if service == 'install':
        late_orders_count = models.Service.objects.install().annotate(
            created_date=Cast('created_at', DateField())
        ).filter(
            Q(status='new') & Q(created_date__lte=threshold_date)
        ).count()
    elif service == 'repair':
        late_orders_count = models.Service.objects.repair().annotate(
            created_date=Cast('created_at', DateField())
        ).filter(
            Q(status='new') & Q(created_date__lte=threshold_date)
        ).count()
    else:
        late_orders = models.Service.objects.filter(
            created_at__lte=threshold_date, status='new')
        late_orders_count = late_orders.aggregate(count=Count('id'))['count']

    return late_orders_count
