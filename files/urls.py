from django.urls import path
from . import views
urlpatterns = [
    path("export_users", views.export_users_csv, name="export_users"),
    path("export_current_service", views.export_current_service,
         name="export_current_service"),
    path("export_current_quarter_services", views.export_current_quarter_services,
         name="export_current_quarter_services"),
    path("export_customers_data", views.export_customers_data,
         name="export_customers_data"),

    path('export_all_services', views.export_all_services,
         name="export_all_services"),
    path('export_all_quarter', views.export_all_quarter_services,
         name="export_all_quarter_services"),
    path('export_repair_customers',  views.export_repair_customers,
         name="export_repair_customers")
]
