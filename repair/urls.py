from django.urls import path
from . import views

urlpatterns = [
    path('repair_request', views.repair_request, name='repair_request'),
    path('repair_appointment', views.repair_appointment, name='repair_appointment')
]
