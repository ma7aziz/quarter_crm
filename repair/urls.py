from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_index, name="repair_index"),
    path('repair_request', views.repair_request, name='repair_request'),
    path('repair_appointment', views.repair_appointment, name='repair_appointment'),
    path('complete_request', views.complete_request, name="complete_request"),
    path('close_request', views.close_request, name="close_request")
]
