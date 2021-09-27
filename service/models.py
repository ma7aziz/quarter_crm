from datetime import date
from django.db import models
from accounts.models import User
from core.models import Customer
import random
import string
# Create your models here.


class RequestManager(models.Manager):

    def repair(self):
        return self.filter(service_type="repair").filter(hold=False)

    def install(self):
        return self.filter(service_type="install").filter(hold=False)

    def on_hold(self):
        return self.filter(hold=True)

    def install_favourites(self):
        return self.filter(favourite=True).filter(service_type="install").filter(hold=False).exclude(status="done").filter(active=True)

    def new(self):
        # new requests
        return self.filter(status='new')

    def under_process(self):
        return self.filter(status="under_process")

    def done(self):
        return self.filter(status="done")

    def suspended(self):
        return self.filter(status="suspended")


REQUEST_STATUS = [
    ('new', 'جديد'),
    ('under_process', 'قيد التنفيذ'),
    ('done', 'تم'),
    ('closed', 'انتهي'),
]


class Service_request(models.Model):
    CUSTOMER_TYPE = [
        ('cash', 'كاش'),
        ('warranty', 'ضمان')
    ]

    REQUEST_TYPE = (
        ("repair", "صيانة"),
        ("install", "تركيب")
    )

    request_number = models.CharField(blank=True, null=True, max_length=15)
    service_type = models.CharField(
        max_length=10, choices=REQUEST_TYPE)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=25)
    machine_type = models.CharField(max_length=200)
    customer_type = models.CharField(choices=CUSTOMER_TYPE, max_length=10)
    invoice_number = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(
        max_length=25, choices=REQUEST_STATUS, default='new')
    file = models.FileField(upload_to='service/files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.CharField(
        unique=True, max_length=40, blank=True, null=True, editable=False)
    appointment = models.ForeignKey(
        "Appointment", on_delete=models.SET_NULL, null=True, blank=True, related_name="service_appointment")
    hold = models.BooleanField(default=False)
    hold_reason = models.ForeignKey(
        "Hold_reason", on_delete=models.SET_NULL, null=True, blank=True)
    favourite = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    excution_files = models.ManyToManyField(
        "ExcutionFile", blank=True, related_name="service_files")
    objects = RequestManager()

    def save(self, *args, **kwargs):
        if not self.code:
            new_id = random.randint(10000, 99999)
            unique = False
            while not unique:
                if Service_request.objects.all().filter(code=new_id):
                    unique = False
                else:
                    unique = True
                    self.code = new_id

        super(Service_request, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_name


class ExcutionFile(models.Model):
    service = models.ForeignKey(Service_request, on_delete=models.CASCADE)
    file = models.FileField(upload_to="service/files/excution_files")

    def __str__(self):
        return f'excution file for request {self.service.id}'


class AppointmentManager(models.Manager):
    def repair(self):
        return self.filter(service_type="repair")

    def install(self):
        return self.filter(service_type="install")


class Appointment(models.Model):
    STATUS = [
        ('open', 'open'),
        ('closed', 'closed')
    ]
    REQUEST_TYPE = (
        ("repair", "صيانة"),
        ("install", "تركيب")
    )
    service_request = models.ForeignKey(
        Service_request, on_delete=models.CASCADE, related_name="request")
    date = models.DateField()
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    service_type = models.CharField(max_length=100, choices=REQUEST_TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default="open")

    objects = AppointmentManager()

    @property
    def is_past_due(self):
        return date.today() > self.date

    @property
    def is_today(self):
        return date.today() == self.date

    def __str__(self):
        return self.service_request.customer_name


class Hold_reason(models.Model):
    service = models.ForeignKey(
        Service_request, on_delete=models.CASCADE, related_name="service_on_hold")
    file = models.FileField(upload_to="hold_files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    hold_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    reason = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.service} Hold Reason !'


class lateDays(models.Model):
    days = models.IntegerField(default=3)
