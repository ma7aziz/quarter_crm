from django.db import models
from datetime import timedelta, date

class ServiceManager(models.Manager):
    def all(self):
        return self.exclude(archive=True).order_by('-created_at')

    def repair(self):
        return self.all().filter(service_type='repair').order_by('-created_at')

    def install(self):
        return self.all().filter(service_type='install')

    def cash(self):
        return self.filter(customer_type='cash')

    def warranty(self):
        return self.filter(customer_type='warranty')

    def new(self):
        return self.filter(status='new')

    def under_process(self):
        return self.filter(status='under_process')

    def late(self):
        late_services = filter(lambda x: x.late, self.all())

        return late_services

    def hold(self):
        return self.filter(hold=True)

    def archive(self):
        return self.filter(archive=True)
    

class AppointmentManager(models.Manager):
    def upcoming(self):
        today = date.today()
        upcoming_appointments= self.filter(date__gte=today).order_by('date')
        return upcoming_appointments
    
    def upcoming_install(self):
        today = date.today()
        upcoming_appointments= self.filter(date__gte=today, service__service_type = 'install').order_by('date')
        return upcoming_appointments
    
    def upcoming_repair(self):
        today = date.today()
        upcoming_appointments= self.filter(date__gte=today, service__service_type = 'repair').order_by('date')
        return upcoming_appointments
    
    def past(self):
        today= date.today()
        past_appointmanets = self.filter(date__lt = today).order_by('date')
        return past_appointmanets
    
    