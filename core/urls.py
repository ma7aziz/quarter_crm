from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('users', views.all_users, name="all_users"),
    path("create_task", views.create_task, name="create_task"),
    path('update_task', views.update_task, name="update_task"),
    path('delete_task/<int:id>', views.delete_task, name="delete_task"),
    path('customers_data', views.customers, name="customers_data"),
    path('customer/<int:id>', views.customer_details, name="customer_details"),
    path('search', views.search, name="search")

]
