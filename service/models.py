from django.db import models
from .choices import SERVICE_TYPE, CUSTOMER_TYPE, REQUEST_STATUS, SPARE_PART_STATUS
from core.models import Customer
from django.conf import settings
import random
from .utils import generate_ref_number
from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Case, When
from .managers import ServiceManager, AppointmentManager
from core.models import LateDays
import uuid
import os 
# Create your models here.
    
def get_file_path(instance, filename):
    """Generate a unique filename for the uploaded file."""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('files/', filename)



User = settings.AUTH_USER_MODEL

status_ordering = Case(
    When(status='new', then=0),
    When(status='under_process', then=1),
    When(status='done', then=2),
    When(status='completed', then=3),
    output_field=models.IntegerField(),
)



class Service(models.Model):
    ref_number = models.CharField(max_length=15, blank=True, null=True)
    customer = models.CharField(max_length=255  , null = True , blank=True )
    phone_number = models.CharField(max_length=255 , null = True , blank=True )
    address = models.CharField(max_length=255, blank=True, null=True)
    customer_type = models.CharField(
        max_length=15, choices=CUSTOMER_TYPE, default='cash')
    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE)
    machine_type = models.CharField(max_length=100, blank=True, null=True)
    invoice_number = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=15, choices=REQUEST_STATUS, default='new')
    notes = models.CharField(max_length=255, blank=True, null=True)
    company = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='warranty_company')
    ac_count = models.PositiveIntegerField(default= 0, blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    code = models.CharField(unique=True, max_length=12,
                            blank=True, null=True, editable=False)
    favourite = models.BooleanField(default=False)
    hold = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)

    objects = ServiceManager()

    def __str__(self):
        return self.ref_number

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = str(random.randint(1000, 9999))
                if not Service.objects.filter(code=code , archive = False).exists():
                    self.code = code
                    break
        if not self.ref_number:
            self.ref_number = generate_ref_number(self.service_type)
        super().save(*args, **kwargs)

    @property
    def late(self):
        '''
        Return True if order is late 
        late order has passed --latedays settings default == 3 -- and status is still new 
        '''
        days = LateDays.objects.last().days
        three_days_ago = timezone.now() - timedelta(days=days - 1)
        return self.status == 'new' and self.created_at <= three_days_ago and self.hold == False

    def has_open_sp_requests(self):
        '''
        Checks if service has unrecieved spare parts requests 
        '''
        return self.sp_request.filter(status='pending').exists()


class File(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_path)
    cretaed_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return 'Service File '


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    technician = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment_tech')
    date = models.DateField()
    notes = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AppointmentManager()

    def __str__(self):
        return f'{self.service} Appointment !'

    @property
    def today(self):
        today = date.today()
        return self.date == today


class ExcutionFile(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_path)
    cretaed_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.service} exec file . '


class HoldReason(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    reason = models.TextField(max_length=300, blank=True, null=True)
    details = models.TextField(max_length=300 , blank = True , null = True )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hold_canceled_by')
    canceled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.service} Hold Reason !'


class HoldFile(models.Model):
    hold_reason = models.ForeignKey(HoldReason, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_file_path)
    cretaed_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


# spare parts request :
class SparePartRequest(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='sp_request')
    requested_parts = models.CharField(max_length=255, blank=True, null=True)
    details = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(
        max_length=15, choices=SPARE_PART_STATUS, default='pending')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recievied_at = models.DateTimeField(blank=True , null=True)
    recievied_by = models.ForeignKey(User , on_delete=models.SET_NULL , null=True ,blank=True , related_name='sp_recieved')

    class Meta:
        verbose_name = 'Spare Part Reauest'
        verbose_name_plural = 'Spare Part Reauests'

    def __str__(self):
        return f'{self.service} spare part request .'
