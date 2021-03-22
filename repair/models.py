from django.db import models
from accounts.models import User

import random
import string
# Create your models here.


class Repair_request(models.Model):
    CUSTOMER_TYPE = [
        ('cash', 'كاش'),
        ('warranty', 'ضمان')
    ]
    REQUEST_STATUS = [
        ('new', 'جديد'),
        ('under_process', 'قيد التنفيذ'),
        ('done', 'تم'),
        ('suspended', 'معلق')
    ]
    # created_by
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=25)
    machine_type = models.CharField(max_length=200)
    customer_type = models.CharField(choices=CUSTOMER_TYPE, max_length=10)
    invoice_number = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(
        max_length=25, choices=REQUEST_STATUS, default='new')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.CharField(
        unique=True, max_length=40, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.code:
            new_id = random.randint(10000, 99999)
            unique = False
            while not unique:
                if Repair_request.objects.all().filter(code=new_id):
                    unique = False
                else:
                    unique = True
                    self.code = new_id

        super(Repair_request, self).save(*args, **kwargs)

    def __str__(self):
        return self.customer_name


class Appointment(models.Model):
    repair_request = models.ForeignKey(
        Repair_request, on_delete=models.CASCADE)
    date = models.DateField()
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    # created_by
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.repair_request.customer_name
