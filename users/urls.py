from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login' , views.Login.as_view() , name='login') ,
    path('logout' ,LogoutView.as_view()  , name='logout'),
    
    path('user/list' , views.UserList.as_view() , name='user_list'),
    path('user/<int:pk>' , views.UserDetails.as_view() , name='user_details'),
    path('user/new' , views.CreateUser.as_view() , name='create_user'),
    path('user/<int:pk>/delete' , views.DeleteUser.as_view() , name='delete_user'),
    path('user/edit'  , views.EditUserDetails.as_view() , name='edit_user_details'),
    path('user/change_password' , views.ChangeUserPassword.as_view() , name='change_password'),
    
    # validate username 
    path('validate_username' , views.validate_username , name='validate_username')
]
