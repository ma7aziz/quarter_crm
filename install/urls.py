from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="install_index"),
    path('install_request', views.install_request, name="install_request"),
    path('get_order_list', views.get_order_list, name="get_order_list")

]
