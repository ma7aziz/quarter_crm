from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    # def create_superuser(self, email, password, **extra_fields):
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     extra_fields.setdefault('role', 1)

    #     return self._create_user(email, password, **extra_fields)


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

    ROLE = (
        (1, 'admin'),
        (2, 'supervisor'),
        (3, 'technician')
    )
    name = models.CharField(_('الاسم'), max_length=100, blank=True)
    username = models.CharField(_('اسم المستخدم'), max_length=25, unique=True)
    phone = models.CharField(_('الجوال'), unique=True, max_length=15)
    role = models.PositiveSmallIntegerField(
        _('الوظيفة'), choices=ROLE, default=1)
    section = models.ManyToManyField(Section)
    created = models.DateTimeField(auto_now_add=True)

    # objects = UserManager()

    def __str__(self):
        return self.username
