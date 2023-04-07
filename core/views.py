from datetime import datetime, timedelta

from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from quarter.models import QuarterProject
from service.models import Appointment, Service, SparePartRequest
from service.utils import get_late_count

from . import models
from .filters import CustomerFilter
from .forms import CustomerForm
from .models import LateDays
from .utils import generate_report


class Index(generic.View):
    def get(self, request):
        template = ''
        ctx = {}

        if request.user.role == 'admin' or request.user.is_superuser:
            counts = Service.objects.aggregate(
                total_counts=Count('id'),

                repair_count=Count('id', filter=Q(service_type='repair')),
                repair_new_count=Count('id', filter=Q(
                    service_type='repair', status='new', hold=False)),
                install_count=Count('id', filter=Q(service_type='install')),
                install_new_count=Count('id', filter=Q(
                    service_type='install', status='new', hold=False)),
                new_count=Count('id', filter=Q(status='new', hold=False)),
                under_process_count=Count(
                    'id', filter=Q(status='under_process')),
                on_hold_count=Count('id', filter=Q(hold=True))
            )
            quarter = QuarterProject.objects.aggregate(total_count=Count('id'),
                                                       new_count=Count('id',  filter=Q(status='new')))
            new_requests = Service.objects.all().filter(status='new', hold=False)
            template = 'core/index.html'
            ctx = {
                'total_count': counts['total_counts'] + quarter['total_count'],
                'quarter_count': quarter['total_count'],
                'quarter_new_count': quarter['new_count'],
                'repair_count': counts['repair_count'],
                'repair_new_count': counts['repair_new_count'],
                'install_count': counts['install_count'],
                'install_new_count': counts['install_new_count'],
                'new_count': counts['new_count'],
                'under_process_count': counts['under_process_count'],
                'on_hold_count': counts['on_hold_count'],
                'new_requests': new_requests,
                'late_count': get_late_count('all')

            }
        elif request.user.role == 'sales':
            template = 'core/sales_index.html'
            counts = Service.objects.filter(created_by=request.user).aggregate(
                total_count=Count('id'),
                repair_count=Count('id', filter=Q(service_type='repair')),
                repair_new_count=Count('id', filter=Q(
                    service_type='repair', status='new')),
                install_count=Count('id', filter=Q(service_type='install')),
                install_new_count=Count('id', filter=Q(
                    service_type='install', status='new')),
                new_count=Count('id', filter=Q(status='new')),
                under_process_count=Count(
                    'id', filter=Q(status='under_process')),
                on_hold_count=Count('id', filter=Q(status='hold'))

            )
            ctx = {
                'total_count': counts['total_count'],
                'repair_count': counts['repair_count'],
                'repair_new_count': counts['repair_new_count'],
                'install_count': counts['install_count'],
                'install_new_count': counts['install_new_count'],
                'new_count': counts['new_count'],
                'under_process_count': counts['under_process_count'],
                'on_hold_count': counts['on_hold_count'],
                'services': Service.objects.filter(created_by=request.user)
            }
        elif request.user.role == 'company':
            template = 'core/company_index.html'
            ctx = {
                'services': Service.objects.filter(created_by=request.user),
                'warranty': Service.objects.repair().filter(company=request.user),
                'sp_requests': SparePartRequest.objects.all().filter(service__company=request.user)
            }
        elif request.user.role == 'technician':
            template = 'core/tech_index.html'
            ctx = {
                'upcoming_appointments': Appointment.objects.upcoming().filter(technician=request.user),
                'past_appointmanets': Appointment.objects.past().filter(technician=request.user),
                'services': Service.objects.all().filter(created_by=request.user)
            }
        elif request.user.role == 'repair_supervisor':
            return redirect(reverse_lazy('service:repair'))
        elif request.user.role == 'install_supervisor':
            return redirect(reverse_lazy('service:install'))
        elif request.user.role in ['quarter_supervisor', 'accountant', 'quarter_sales', 'egypt_office']:
            return redirect(reverse_lazy('quarter:project_list'))
        return render(request, template, ctx)


class CustomerList(generic.ListView):
    model = models.Customer
    template_name = 'core/customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        print(self.request.GET)
        qs = super().get_queryset()
        if self.request.user.role == 'sales':
            qs = self.model.objects.filter(created_by=self.request.user)
        self.filterset = CustomerFilter(self.request.GET, queryset=qs)
        return self.filterset.qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        kwargs['customer_form'] = CustomerForm
        kwargs['filterform'] = self.filterset.form
        return super().get_context_data(**kwargs)


class CreateCustomerView(generic.CreateView):
    model = models.Customer
    fields = ['name', 'phone_number', 'address', 'city']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, 'تم اضافة العميل !')
        return redirect(self.request.META.get('HTTP_REFERER'))


class CustomerDetails(generic.DetailView):
    model = models.Customer
    lookup_field = 'pk'
    context_object_name = 'customer'
    template_name = 'core/customer_details.html'


class Archive(generic.ListView):

    '''
    List all aarchived services 
    service is archived after 30 days if status == closed
    '''
    template_name = 'service/archive.html'
    model = Service
    context_object_name = 'services'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Service.objects.archive()
        elif self.request.user.role == 'install_supervisor':
            qs = Service.objects.archive().filter(service_type='install')
        elif self.request.user.role == 'repair_supervisor':
            qs = Service.objects.archive().filter(service_type='repair')
        else:
            qs = self.request.user.service_set.filter(archive=True)
        print(qs.explain())
        return qs


class Reports(generic.View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_data')

        report = generate_report(start_date, end_date)
        ctx = {
            'report': report,

        }
        return render(request, 'core/reports.html', ctx)


# dashboard htmx
def index_data(request):
    '''
    Htmx tables in index page 
    repair == new , current 
    install == new , current 
    hold  
    '''
    service_type = request.GET['service']
    base_temp_name = 'core/partials/htmx/'
    if service_type == 'install':
        template = base_temp_name + 'install.html'
        ctx = {
            'services': Service.objects.install().filter(Q(status='new') | Q(status='under_process'))
        }
    elif service_type == 'repair':
        template = base_temp_name + 'repair.html'
        ctx = {
            'services': Service.objects.repair().filter(Q(status='new') | Q(status='under_process'))
        }
    elif service_type == 'hold':
        template = base_temp_name + 'hold.html'
        ctx = {
            'services': Service.objects.repair().filter(hold=True)
        }
    elif service_type == 'late':
        template = base_temp_name + 'late.html'
        days = LateDays.objects.last().days
        days_ago = timezone.now() - timedelta(days=days - 1)
        late_orders = Service.objects.filter(
            status='new', created_at__lte=days_ago)

        ctx = {
            'services': late_orders,
        }
    elif service_type == 'quarter':
        template = base_temp_name + 'quarter.html'
        ctx = {
            'services': QuarterProject.objects.all()
        }
    elif service_type == 'all':
        template = base_temp_name + 'all.html'
        quarter = QuarterProject.objects.all().filter(status='new')
        service = Service.objects.new()

        ctx = {
            'services': service,
            'quarter': quarter
        }

    return render(request, template, ctx)


class ServiceChartView(generic.View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        data = Service.objects.filter(created_at__gte=start_date, created_at__lte=end_date).values(
            'service_type').annotate(count=Count('id'))

        service_labels = [item['service_type'] for item in data]
        service_counts = [item['count'] for item in data]

        # Quarter
        quarter = QuarterProject.objects.filter(
            created_at__gte=start_date, created_at__lte=end_date)
        quarter_lable = ['Qurater']
        quarter_counts = [quarter.count()]
        labels = service_labels + quarter_lable
        counts = service_counts + quarter_counts
        return JsonResponse({'labels': labels, 'counts': counts})


class SalesPerformance(generic.View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        data = Service.objects.filter(created_at__gte=start_date, created_at__lte=end_date).values(
            'created_by__username').annotate(count=Count('id'))
        labels = [item['created_by__username'] for item in data]
        counts = [item['count'] for item in data]
        return JsonResponse({'labels': labels, 'counts': counts})


class DailyPerformance(generic.View):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        data = Service.objects.filter(created_at__gte=start_date, created_at__lte=end_date).annotate(
            date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        labels = [d['date'].strftime('%Y-%m-%d') for d in data]
        counts = [d['count'] for d in data]
        return JsonResponse({'labels': labels, 'counts': counts})
