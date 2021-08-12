from django.urls import path
from . import views
urlpatterns = [
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit_user', views.edit_user, name="edit_user"),
    path('delete_user/<str:username>',
         views.delete_user, name="delete_user"),
    path('new_tasks', views.new_tasks, name='new_tasks'),
    path('history', views.history, name='history'),
    path('change_password', views.change_password, name="change_password"),
    path("reset_password", views.reset_password, name="reset_password"),
    path('edit_qouta', views.edit_qouta, name='edit_qouta'),
    path('edit_services_allowed', views.edit_services_allowed,
         name="edit_services_allowed")
]
