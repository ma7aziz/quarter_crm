from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="quarter_index"),
    path('create_request', views.create_request, name="new_quarter_request"),
    path('service/<int:id>', views.request_details,
         name="quarter_request_details"),
    path('pricing', views.pricing, name="pricing"),
    path('confirm_price/<int:id>',  views.confirm_prcie, name="confirm_price"),
    path('first_transfer', views.first_transfer, name="first_transfer"),

]
