from django.db import models
from accounts.models import User
from .choices import STATUS_CHOICES
# Create your models here.


class Quarter_service_Manager(models.Manager):
    def all(self):
        return self.filter(active=True)

    def new(self):
        return self.filter(status="new")


class Quarter_service(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(
        default=1, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    pricing = models.ForeignKey(
        "Price", on_delete=models.SET_NULL, null=True, blank=True)
    money_transfer = models.ForeignKey(
        "Transfer", on_delete=models.SET_NULL, null=True, blank=True)
    designs = models.ForeignKey(
        "Design", on_delete=models.SET_NULL, null=True, blank=True)
    objects = Quarter_service_Manager()

    def __str__(self):
        return f'{self.name}'


class Price(models.Model):
    service = models.ForeignKey(Quarter_service, on_delete=models.CASCADE)
    price = models.CharField(max_length=6, blank=True)
    files = models.FileField(upload_to='pricing/', )
    notes = models.TextField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    ################# STATUS #############

    def __str__(self):
        return self.service.name


class Transfer(models.Model):
    service = models.ForeignKey(Quarter_service, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    # transfer 1
    transfer1_qty = models.IntegerField(default=0)
    transfer1_date = models.DateTimeField(blank=True, null=True)
    transfer1_file = models.FileField(
        upload_to='transfer/', blank=True, null=True)
    transfer1_notes = models.TextField(max_length=500, blank=True)
    # transfer 2
    transfer2_qty = models.IntegerField(default=0)
    transfer2_date = models.DateTimeField(blank=True, null=True)
    transfer2_file = models.FileField(
        upload_to='transfer/', blank=True, null=True)
    transfer2_notes = models.TextField(max_length=500, blank=True)
    # transfer 3
    transfer3_qty = models.IntegerField(default=0)
    transfer3_date = models.DateTimeField(blank=True, null=True)
    transfer3_file = models.FileField(
        upload_to='transfer/', blank=True, null=True)
    transfer3_notes = models.TextField(max_length=500, blank=True)

    outstanding_ammount = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.outstanding_ammount = self.total_price - \
            (self.transfer1_qty + self.transfer2_qty + self.transfer3_qty)

        super(Transfer, self).save(*args, **kwargs)


class Design(models.Model):
    service = models.ForeignKey(Quarter_service, on_delete=models.CASCADE)
    files = models.FileField(upload_to='designes/', blank=True,  null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Designes for {self.service}"
