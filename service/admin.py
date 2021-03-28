from django.contrib import admin

# Register your models here.
from .models import Service_request, Appointment
# Register your models here.
admin.site.register(Service_request)
admin.site.register(Appointment)
