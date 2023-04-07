from django.urls import path
from . import views

app_name = 'quarter'
urlpatterns = [
    path('' , views.ProjectList.as_view() , name='project_list'),
    path('new' , views.CreateProject.as_view() , name='create_project'),
    path('project/<int:pk>' , views.ProjectDetails.as_view() , name='project_details'),
    path('project/<int:pk>/update' , views.UpdateProject.as_view() , name='update_project'),
    path('project/<int:pk>/delete' , views.DeleteProject.as_view() , name='delete_project'),
    path('project/start_negotiation' , views.StartNegotiation.as_view() , name='start_negotiation'),
    path('project/negotiation_status' , views.NegotiationStatus.as_view() , name='negotiation_status'),
    path('project/attach_files' , views.AttachExcutionFiles.as_view() , name='attach_files'),
    path('project/confirm_project' , views.ConfirmProject.as_view() , name='confirm_project'),
    path('data' , views.get_data, name='get_data')
]
