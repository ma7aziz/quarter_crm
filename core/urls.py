from . import views
from django.urls import path


app_name = 'core'
urlpatterns = [
    path('' , views.Index.as_view() ,name='index'),
    path('customers' , views.CustomerList.as_view() , name='customer_list'),
    path('customers/new' , views.CreateCustomerView.as_view() , name='add_customer'),
    path('customers/<int:pk>/details' , views.CustomerDetails.as_view() , name='customer_details'),
    path('archive' , views.Archive.as_view() , name='archive'),
    path('reports' , views.Reports.as_view() , name='reports'),
    path('index_data' , views.index_data , name='index_data'),
    
    path('service_chart' , views.ServiceChartView.as_view() , name='service_chart_view'),
    path('sales_performance_chart' , views.SalesPerformance.as_view() , name='sales_performance_chart'),
    path('daily_performance_chart' , views.DailyPerformance.as_view() , name='daily_performance_chart'),
]
