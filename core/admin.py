from django.contrib import admin

# Register your models here.
from .models import Task, Customer , Upload

admin.site.register(Task)
admin.site.register(Customer)
admin.site.register(Upload)
