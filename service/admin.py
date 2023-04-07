from django.contrib import admin
from . import models 
# Register your models here.

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['ref_number' , 'archive' , 'favourite']
    list_editable = ['archive' , 'favourite']


admin.site.register(models.Service , ServiceAdmin)
admin.site.register(models.File)
admin.site.register(models.SparePartRequest)