from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="quarter_index"),
    path('create_request', views.create_request, name="new_quarter_request"),
    path('service/<int:id>', views.request_details,
         name="quarter_request_details"),
    path('delete/<int:id>', views.delete_request, name="delete_quarter_request"),
    path('change_status', views.change_status, name="change_quarter_status"),
    path('hold_quarter_request/<int:id>',
         views.hold_request, name="hold_quarter_request"),
    path('deactivate_quarter/<int:id>',
         views.deactivate_request, name="deactivate_quarter"),
    path('quarter_multi_delete', views.quarter_multi_delete,
         name="quarter_multi_delete"),
    path('pricing', views.pricing, name="pricing"),
    path('confirm_process/<int:id>',
         views.confirm_process, name="confirm_process"),
    path('first_transfer', views.first_transfer, name="first_transfer"),
    path('second_transfer', views.second_transfer, name="second_transfer"),
    path('attach_designs', views.attach_designs, name="attach_designs"),
    path('attach_purchase', views.attach_purchase, name="attach_purchase"),
    path('end_request/<int:id>', views.end_request, name="end_request"),
    path('reject_price', views.reject_price, name="reject_price"),
    path('edit_request', views.edit_request, name="edit_quarter_request"),
    path('attach_excution_files' , views.attach_excution_files ,  name="attach_excution_files")

]
