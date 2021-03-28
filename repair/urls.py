from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_index, name="repair_index"),
    path('repair_request', views.repair_request, name='repair_request'),

]
