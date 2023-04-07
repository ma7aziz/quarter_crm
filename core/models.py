from django.db import models
from django.conf import settings


# Create your models here.
User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    name = models.CharField(max_length=255 ) 
    phone_number = models.CharField(max_length= 15 , unique = True )
    address = models.CharField(max_length= 255 , blank=True)
    city = models.CharField(max_length=50 , blank=True)
    created_by = models.ForeignKey(User , on_delete=models.SET_NULL , null =True , blank = True )
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    

class LateDays(models.Model):
    days = models.PositiveIntegerField(default=3)
    
    class Meta:
        verbose_name_plural = 'Late Days'
    
    def __str__(self):
        return f'late days are {self.days}'