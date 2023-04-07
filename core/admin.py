from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Customer)


@admin.register(models.LateDays)
class LateDaysAdmin(admin.ModelAdmin):
    '''
    Prevent adding or deleting any instances of late days 
    
    '''
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


