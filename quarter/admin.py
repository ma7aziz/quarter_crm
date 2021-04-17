from django.contrib import admin
from .models import Quarter_service, Price, Transfer, Design
# Register your models here.
admin.site.register(Quarter_service)
admin.site.register(Price)
admin.site.register(Transfer)
admin.site.register(Design)
