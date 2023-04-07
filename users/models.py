from django.db import models
from django.contrib.auth.models import AbstractUser , UserManager
from .choices import USER_ROLES
from django.utils import timezone

# Create your models here.

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('install' , True)
        extra_fields.setdefault('repair' , True)
        extra_fields.setdefault('quarter' , True)
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=125 , blank= True )
    phone_number = models.CharField(max_length=15  , blank=True)
    role = models.CharField(choices=USER_ROLES , default='sales' , max_length=25)
    profile_pic = models.ImageField(upload_to='users/profile_pics' , blank=True , null=True )
    favourite_qouta = models.PositiveIntegerField(default=3)
    install = models.BooleanField(default=False)
    repair = models.BooleanField(default=False)
    quarter = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    
    def save(self, *args , **kwargs) -> None:
        if self.role == 'install_supervisor':
            self.install = True 
        if self.role == 'repair_supervisor' : 
            self.repair = True 
        if self.role in ['quarter_supervisor' , 'accountant' , 'excution' , 'quarter_sales' ]:
            self.quarter = True 
        return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.username
    

    
    @property
    def remaining_qouta(self):
        '''
        Returns the remaining install qouta for the day 
        '''
        today = timezone.now().date()
        used_qouta = self.service_set.filter(service_type = 'install' , favourite = True , created_at__date=today).count()
        remaining = self.favourite_qouta - used_qouta
        
        return remaining