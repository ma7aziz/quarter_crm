from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
# Create your models here.


class UserManager(BaseUserManager):
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(MyForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class Section(models.Model):
    ALL = 1
    INSTALL = 2
    REPAIR = 3
    QUARTER = 4
    SECTION_CHOICES = [
        (1, 'all'),
        (2, 'install'),
        (3, 'repair'),
        (4, 'quarter')
    ]
    id = models.PositiveIntegerField(choices=SECTION_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    ADMIN = 1
    SUPERVISOR = 2
    TECHNICIAN = 3
    SALES = 4

    ROLE = (
        (1, 'admin'),
        (2, 'supervisor'),
        (3, 'technician'),
        (4, 'sales')
    )
    name = models.CharField(_('الاسم'), max_length=100, blank=True)
    phone = models.CharField(_('الجوال'),
                             max_length=15, blank=True)
    role = models.PositiveSmallIntegerField(
        _('الوظيفة'), choices=ROLE, default=1)
    section = models.ManyToManyField(Section)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
