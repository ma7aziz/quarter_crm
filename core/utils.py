
from django.db.models import Count , Sum
from service.models import Service , Appointment
from quarter.models import QuarterProject
from django.utils import timezone
from datetime import datetime
import uuid

def generate_report(start_date = None , end_date = None):

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if end_date:

        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = timezone.now()

        # Get the count of services done between certain dates
    services = Service.objects.filter(created_at__range=[start_date, end_date] )
    quarter = QuarterProject.objects.filter(created_at__range=[start_date , end_date])
    quarter_count =  quarter.count()
    total_count = services.count() + quarter_count
    repair_count = services.filter(service_type='repair').count()
    install_count = services.filter(service_type='install').count()
    top_sales = services.values('created_by__username').annotate(sales=Count('id')).order_by('-sales')
    
    
    # technicians 
    appointments = Appointment.objects.filter(date__range=[start_date , end_date])
    top_techs = appointments.values('technician__username' ).annotate(
        appointments = Count('id'),
        ac_count=Sum('service__ac_count')
    )
    return {
        'start_date': start_date , 
        'end_date' : end_date,
        'total_count': total_count,
        'repair_count': repair_count,
        'install_count': install_count,
        'quarter_count' : quarter_count , 
        'top_sales': top_sales,
        'top_techs' : top_techs
    }
    
