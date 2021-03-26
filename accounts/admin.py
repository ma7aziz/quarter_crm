from django.contrib import admin
from .models import User, Section
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

admin.site.register(User)
# admin.site.register(CustomUserAdmin)
admin.site.register(Section)
