from django.urls import path
from . import views
urlpatterns = [
    path("export_users", views.export_users_csv, name="export_users"),
    path("export_current_service", views.export_current_service,
         name="export_current_service"),
    path("export_current_quarter_services", views.export_current_quarter_services,
         name="export_current_quarter_services"),
    path("export_customers_data", views.export_customers_data,
         name="export_customers_data")
]
