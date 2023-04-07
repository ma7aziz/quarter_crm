from django.urls import path
from . import views


app_name = 'service'
urlpatterns = [
    
    path('' , views.ServiceListView.as_view() , name = 'service_list'),
    path('new' , views.CreateService.as_view() , name = 'add_service'),
    path('<int:pk>/details' , views.ServiceDetails.as_view() , name = 'service_details'),
    path('<int:pk>/delete' , views.DeleteService.as_view() , name='delete_service') ,
    path('update_status' , views.UpdateServiceStatus.as_view() , name='update_service_status') ,
    path('hold_service' , views.HoldService.as_view() , name='hold_service') ,
    path('favourite_service' , views.FavouriteService.as_view() , name='favourite_service'),
    path('set_appointment' , views.SetAppointment.as_view() , name='set_appointment'),
    path('confirm_excution' , views.ConfirmExcution.as_view() , name='confirm_excution'),
    path('spare_part_request' , views.SparePartRequest.as_view() , name='spare_part_request'),
    path('sp/confirm_recieve' , views.ConfirmSparePartRecieve.as_view() , name='confirm_sp_recievce') , 
    path('install' , views.InstallListView.as_view() , name='install'),
    path('repair' , views.RepairListView.as_view() , name='repair'),
    # htmx views 
    path('service_request' , views.service_request , name='service_request'),
    path('get_data' , views.render_service_data , name='get_data')
]
