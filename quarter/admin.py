from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.QuarterProject)
admin.site.register(models.ProjectFiles)
admin.site.register(models.File)