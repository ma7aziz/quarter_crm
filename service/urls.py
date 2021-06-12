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
    path('close_request', views.close_request, name="close_request"),
    path('deactivate_request/<int:id>',
         views.deactivate_request, name="deactivate_request"),
    path('delete_request/<int:id>', views.delete_request, name="delete_request"),
    path('hold_request/<int:id>', views.hold, name='hold_request'),
    path('change_status', views.change_status, name="change_request_status"),
    path('service_multiple_delete', views.multiple_delete,
         name="service_multiple_delete"),
    path('favorite/<int:id>', views.favorite, name="favorite"),
    path('change_late_days' , views.change_late_days , name= "change_days"),
    path("chcek_favorite" , views.check_favorite , name="check_favorite")
]
