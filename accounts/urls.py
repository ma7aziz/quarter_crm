from django.urls import path
from . import views
urlpatterns = [
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit_user', views.edit_user, name="edit_user"),
    path('delete_user/<str:username>',
         views.delete_user, name="delete_user")
]