from django.urls import path
from . import views
urlpatterns = [
    path('service_request_detils/<int:id>',
         views.service_request_details, name="service_request_details"),
    path('service_appointment', views.service_appointment,
         name='repair_appointment'),
    path('change_appointment', views.change_appointment,
         name="change_repair_appointment"),
    path('appointment/<int:id>',
         views.appointment_details, name="appointment_details"),
    path('complete_request', views.complete_request, name="complete_request"),
    path('close_request', views.close_request, name="close_request")
]