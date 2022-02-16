from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_index, name="repair_index"),
    path('repair_request', views.repair_request, name='repair_request'),
    path("spare_part_request" , views.spare_request , name="spare_part_request"),
    path("spare_request_details/<int:id>" , views.spare_request_details , name="spare_request_details"),
    path("end_spare_request/<int:id>" , views.change_spare_request_status, name="change_spare_request_status"),
    path("delete_spare_request/<int:id>" , views.delete_spare_request , name="delete_spare_request")

]
