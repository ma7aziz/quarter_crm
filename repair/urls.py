from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_index, name="repair_index"),
    path('repair_request', views.repair_request, name='repair_request'),
    path('repair_request_detils/<int:id>',
         views.repair_request_details, name="repair_request_details"),

    path('repair_appointment', views.repair_appointment, name='repair_appointment'),
    path('change_appointment', views.change_appointment,
         name="change_repair_appointment"),
    path('repair_appointment/<int:id>',
         views.appointment_details, name="appointment_details"),
    path('complete_request', views.complete_request, name="complete_request"),
    path('close_request', views.close_request, name="close_request")
]
