from django.db import models
from accounts.models import User

import random
import string
# Create your models here.


class RequestManager(models.Manager):
    def repair(self):
        return self.filter(service_type="repair")

    def install(self):
        return self.filter(service_type="install")

    def new(self):
        # new requests
        return self.filter(status='new')

    def under_process(self):
        return self.filter(status="under_process")

    def done(self):
        return self.filter(status="done")

    def suspended(self):
        return self.filter(status="suspended")


class Service_request(models.Model):
    CUSTOMER_TYPE = [
        ('cash', 'كاش'),
        ('warranty', 'ضمان')
    ]
    REQUEST_STATUS = [
        ('new', 'جديد'),
        ('under_process', 'قيد التنفيذ'),
        ('suspended', 'معلق'),
        ('done', 'تم'),
        ('closed', 'انتهي'),
    ]

    REQUEST_TYPE = (
        ("repair", "repair"),
        ("install", "install")
    )

    service_type = models.CharField(
        max_length=10, choices=REQUEST_TYPE)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    machine_type = models.CharField(max_length=200)
    customer_type = models.CharField(choices=CUSTOMER_TYPE, max_length=10)
    invoice_number = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    notes = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(
        max_length=25, choices=REQUEST_STATUS, default='new')
    file = models.FileField(upload_to='repair/files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.CharField(
        unique=True, max_length=40, blank=True, null=True, editable=False)

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


class Appointment(models.Model):
    STATUS = [
        ('open', 'open'),
        ('closed', 'closed')
    ]
    service_request = models.ForeignKey(
        Service_request, on_delete=models.CASCADE)
    date = models.DateField()
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default="open")

    def __str__(self):
        return self.service_request.customer_name