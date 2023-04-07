from django.urls import path
from . import views 


app_name = 'api'
urlpatterns = [
    path('customers' , views.CustomerList.as_view() , name='customer_list')   ,
    path('sp_request/<int:pk>' , views.SparePartRequestDetails.as_view() , name='sp_request_details')    ,
]
