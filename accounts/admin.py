from django.contrib import admin
from .models import User, Section, Qouta
from django.contrib.auth.admin import UserAdmin


# Register your models here.

admin.site.register(User)
# admin.site.register(CustomUserAdmin)
admin.site.register(Section)
admin.site.register(Qouta)
