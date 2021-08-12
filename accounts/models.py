from django.db import models
import datetime

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

    def sales(self):
        sales = self.filter(role=4)
        return sales


class Section(models.Model):
    ALL = 1
    INSTALL = 2
    REPAIR = 3
    QUARTER = 4
    SECTION_CHOICES = [
        (1, 'جميع الأقسام'),
        (2, 'التركيب'),
        (3, 'الصيانة'),
        (4, 'كوارتر ')
    ]
    id = models.PositiveIntegerField(choices=SECTION_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


ADMIN = 1
INSTALL_SUPERVISOR = 2
REPAIR_SUPERVISOR = 3
QUARTER_SUPERVISOR = 4
SALES = 5
ACCOUNTANT = 6
EGYPT_OFFICE = 7
TECHNICIAN = 8
EXCUTION = 9

ROLE = (
    (1, 'مدير الموقع'),
    (2, 'مدير التركيبات'),
    (3, 'مدير الصيانة'),
    (4, 'مشرف كوارتر '),
    (5, 'مندوب بيع '),
    (6, 'حسابات'),
    (7, 'مكتب مصر '),
    (8, 'فني '),
    (9, "تنفيذ كوارتر")

)


class User(AbstractUser):
    name = models.CharField(_('الاسم'), max_length=100, blank=True)
    phone = models.CharField(_('الجوال'),
                             max_length=15, blank=True)
    role = models.PositiveSmallIntegerField(
        _('الوظيفة'), choices=ROLE, default=1)
    completed_tasks = models.IntegerField(default=0)
    submitted_orders = models.IntegerField(default=0)
    profile_pic = models.ImageField(
        upload_to="user_data/profile_pics", blank=True, null=True)
    files = models.FileField(
        upload_to="user_data/files", blank=True, null=True)
    # can add quarter
    quarter = models.BooleanField(default=False)
    # can add repair
    repair = models.BooleanField(default=False)
    # can add install
    install = models.BooleanField(default=True)
    favourite_qouta = models.ForeignKey(
        'Qouta', on_delete=models.SET_NULL, null=True, blank=True, related_name='favourite_count')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Qouta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    max_requests = models.SmallIntegerField(default=1)
    current_requests = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.user}'
