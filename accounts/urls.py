from django.urls import path
from . import views
urlpatterns = [
    path('profile/<str:username>', views.profile, name='profile'),
    path('delete_user/<str:username>',
         views.delete_user, name="delete_user")
]
