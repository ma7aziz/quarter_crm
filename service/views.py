from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from . import models
from django.contrib import messages
from core.forms import CustomerForm
from . import choices
from django.db import transaction
import datetime
from users.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Count, Q 
from django.db import models as md
from core.decorators import allowed_roles
from django.utils.decorators import method_decorator
from .utils import get_late_count

# Create your views here.
@method_decorator(allowed_roles(['admin']), name='dispatch')
class ServiceListView(generic.ListView):
    model = models.Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        status_ordering = Case(
            When(status='new', then=0),
            When(status='under_process', then=1),
            When(status='done', then=2),
            When(status='completed', then=3),
            output_field=md.IntegerField(),
        )
        queryset = super().get_queryset().order_by(
            status_ordering,
            '-favourite',
            'created_at',
        )
        if self.request.user.role == 'sales':
            queryset = queryset.filter(created_by=self.request.user)

        # Order by Favourite first, only if the status is 'new'
        queryset = queryset.annotate(fav_first=Case(
            When(status='new', favourite=True, then=True),
            default=False,
            output_field=md.BooleanField(),
        )).order_by(status_ordering, '-fav_first')
        return queryset


@method_decorator(allowed_roles(['admin', 'install_supervisor']), name='dispatch')
class InstallListView(generic.ListView):
    model = models.Service
    template_name = 'service/install.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = models.Service.objects.install()
        queryset = queryset.annotate(
                fav_new_first=Case(
                    When(status='new', favourite=True, then=True),
                    default=False,
                    output_field=md.BooleanField(),
                ),
            ).order_by( '-fav_new_first'  , models.status_ordering  , '-created_at' )
        if self.request.user.role == 'sales':
            queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        counts = models.Service.objects.install().aggregate(
            total_count=Count('id'),
            on_hold_count=Count('id', filter=Q(hold=True)),
            new_count=Count('id', filter=Q(status='new')),
            under_process_count=Count('id', filter=Q(
                status='under_process', hold=False)),
            new_favs=Count('id', filter=Q(status='new', favourite=True)),
            current_favs=Count('id', filter=Q(
                status='under_process', favourite=True, hold=False)),
        )
        kwargs.update(counts)

        kwargs['upcoming_appointments_count'] = models.Appointment.objects.upcoming_install(
        ).only('id').count()
        kwargs['late_count'] = get_late_count('install')
        return super().get_context_data(**kwargs)


@method_decorator(allowed_roles(['admin', 'repair_supervisor']), name='dispatch')
class RepairListView(generic.ListView):
    model = models.Service
    template_name = 'service/repair.html'
    context_object_name = 'services'

    def get_queryset(self):

        queryset = models.Service.objects.repair().order_by(
            models.status_ordering, '-created_at')
        if self.request.user.role == 'sales':
            queryset = queryset.filter(created_by=self.request.user)

        queryset = queryset.annotate(fav_first=Case(
            When(status='new', favourite=True, then=True),
            default=False,
            output_field=md.BooleanField(),
        )).order_by(models.status_ordering, '-fav_first')
        return queryset

    def get_context_data(self, **kwargs):

        counts = models.Service.objects.repair().aggregate(
            total_count=Count('id'),
            on_hold_count=Count('id', filter=Q(hold=True)),
            new_count=Count('id', filter=Q(status='new')),
            under_process_count=Count('id', filter=Q(
                status='under_process',  hold=False)),
            new_favs=Count('id', filter=Q(status='new', favourite=True)),
            current_favs=Count('id', filter=Q(status='under_process', favourite=True,   hold=False)))
        kwargs.update(counts)
        kwargs['upcoming_appointments_count'] = models.Appointment.objects.upcoming_repair(
        ).only('id').count()
        kwargs['late_count'] = get_late_count('repair')
        return super().get_context_data(**kwargs)


class CreateService(generic.CreateView):
    '''
    create new service request 
    use form 
    validation is done in the frontend and back end 
    '''
    model = models.Service
    fields = ['customer', 'address', 'customer_type', 'favourite', 'phone_number',
              'service_type', 'machine_type', 'invoice_number', 'notes' , 'ac_count']
    success_url = reverse_lazy('core:index')
    template_name = 'service/service_create.html'

    def get_success_url(self) :
        if self.request.POST['service_type'] == 'install': 
            return reverse_lazy('service:install')
        elif self.request.POST['service_type'] == 'repair' :
            return reverse_lazy('service:repair')



    def get_context_data(self, **kwargs):
        kwargs['customer_form'] = CustomerForm
        kwargs['companies'] = User.objects.filter(role='company')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if self.request.POST.getlist('favourite'):
            form.instance.favourite = True
        if self.request.POST.getlist('company'):
            company = User.objects.get(pk=self.request.POST['company'])
            form.instance.company = company
        service = form.save()  # Save the Service instance first
        if self.request.FILES:
            files = self.request.FILES.getlist('file')
            for f in files:
                file_instance = models.File(service=service, file=f)
                file_instance.save()
        messages.success(self.request, 'تم اضافة الطلب بنجاح !')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'حدث خطأ .. يرجي المحاولة مرة اخري  !')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ServiceDetails(generic.DetailView):

    model = models.Service
    lookup_field = 'pk'
    context_object_name = 'service'
    template_name = 'service/service_details.html'

    def get_context_data(self, **kwargs):
        if self.object.hold:
            # print(self.object.holdreason_set.last())
            kwargs['hold_reason'] = self.object.holdreason_set.last()
        if self.object.status == 'under_process':
            kwargs['appointment'] = self.object.appointment_set.last()
        kwargs['technician'] = User.objects.filter(role='technician')
        kwargs['status_choices'] = choices.REQUEST_STATUS
        return super().get_context_data(**kwargs)


class DeleteService(generic.DeleteView):
    model = models.Service
    lookup_field = 'pk'
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف الطلب !')
        return super().form_valid(form)


class UpdateServiceStatus(generic.View):
    def get(self, request):
        print(request.GET)
        try:
            service_id = request.GET.get('service')
            status = request.GET.get('status')
            if service_id and status:
                service = get_object_or_404(models.Service, id=service_id)
                if status == 'closed':
                    service.status = 'closed'
                    service.save()
                    messages.success(request, 'تم اغلاق الطلب ')
                    return redirect(reverse_lazy('core:index'))
        except Exception as e:
            print(e)
            messages.error(request, 'خطأ')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request):
        service = models.Service.objects.get(pk=request.POST['service'])
        if not service.status == request.POST['status']:
            service.status = request.POST['status']
            service.save()
            messages.success(request, 'تم تحديث حالة الطلب !')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class HoldService(generic.View):
    def post(self, request):
        try:
            with transaction.atomic():
                service = models.Service.objects.get(
                    pk=request.POST['service'])
                if not service.hold:
                    hold_reason = models.HoldReason(
                        service=service,
                        details=request.POST['hold_reason'],
                        created_by=request.user
                    )
                    hold_reason.save()
                    service.hold = True
                    service.status = 'under_process'
                    service.save()
                    if self.request.FILES:
                        files = self.request.FILES.getlist('file')
                        for f in files:
                            file_instance = models.HoldFile(
                                hold_reason=hold_reason, file=f, created_by=request.user)
                            file_instance.save()

                    if request.POST['reason'] == 'spare_parts':
                        hold_reason.reason = 'طلب قطع غيار '
                        hold_reason.save()
                        sp_request = models.SparePartRequest(
                            service=service,
                            requested_parts=request.POST['spare_parts'],
                            details=request.POST['hold_reason'],
                            created_by=request.user)
                        sp_request.save()
                    
                    messages.success(request, 'تم تعليق الطلب !')

                else:
                    # unhold service .. change service status , cancel hold reason by user at time
                    hold_reason = models.HoldReason.objects.get(
                        pk=request.POST['hold_reason'])
                    hold_reason.canceled_by = request.user
                    hold_reason.canceled_at = datetime.datetime.now()
                    hold_reason.save()
                    service.hold = False
                    service.save()
                    messages.success(request, 'تم اعادة تفعيل الطلب !!')

        except Exception as e:
            messages.error(
                request, 'An error occurred while processing your request: {}'.format(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# favourite / unvaforite


class FavouriteService(generic.View):
    def post(self, request):
        service = models.Service.objects.get(pk=request.POST['service'])
        if service.favourite:
            service.favourite = False
            service.save()
            messages.success(request, 'تم الازالة من المفضلات .')
        else:
            if request.user.remaining_qouta or request.user.is_superuser or request.user.role == 'install_supervisor':
                service.favourite = True
                service.save()
                messages.success(request, 'تم تفضيل الطلب !')
            else:
                messages.error(
                    request, 'لا يمكنك أضافة طلب جديد الي المفضلات اليوم !!')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# Excution


class SetAppointment(generic.View):
    '''
    Set appointment for service request ,
    done by install or repair manager 
    data : technician , date , notes 
    '''

    def post(self, request):
        with transaction.Atomic(using='default', savepoint=True, durable=False):
            try:
                service = models.Service.objects.get(
                    pk=request.POST['service'])
                technician = User.objects.get(pk=request.POST['technician'])
                appointment = models.Appointment.objects.update_or_create(
                    service=service,
                    defaults={
                        'technician': technician,
                        'date': datetime.datetime.today(),
                        'notes': request.POST['notes']
                    }
                )
                service.status = 'under_process'
                service.save()
                messages.success(request, 'تم تحديد الموعد !')
                if request.POST.getlist('hold_reason'):
                    hold_reason = models.HoldReason.objects.get(
                            pk=request.POST['hold_reason'])
                    hold_reason.canceled_by = request.user
                    hold_reason.canceled_at = datetime.datetime.now()
                    hold_reason.save()
                    service.hold = False
                    service.save()
                    messages.success(request, 'تم  اعادة تفعيل الطلب  !')
            except Exception as e:
                messages.error(request, f'خطأ {e}.. يرجي المحاولة مرة اخري ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# confirm excution by tech, instal supervisor  => change status to done
class ConfirmExcution(generic.View):
    '''
    Confirm service excution 
    need service code if confirmation done by technician 
    if confirm done by admin , supervisor === 0000
    '''

    def post(self, request):
        code = request.POST['code']
        service = models.Service.objects.get(pk=request.POST['service'])
        if code == service.code:
            service.status = 'done'
        elif request.user.role == 'repair_supervisor' or request.user.role == 'install_supervisor' or request.user.is_superuser:
            if code == '0000':
                service.status = 'done'
        else:
            if request.user.role == 'technician':
                messages.error(
                    request, 'يرجي ادخال كود التنفيذ الصحيح أو التواصل مع المشرف')
                messages.error(
                    request, 'Wrong code ! please submit the right code or contact your supervisor !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        service.save()

        if service.status == 'done':
            if request.FILES:
                files = request.FILES.getlist('file')
                for f in files:
                    file_instance = models.ExcutionFile(
                        service=service, file=f, created_by=request.user)
                    file_instance.save()
            messages.success(request, 'تم التحديث !')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SparePartRequest(generic.View):
    def get(self, request, *args, **kwargs):
        template_name = 'service/sp_requests.html'
        ctx = {
            'sp_requests' : models.SparePartRequest.objects.all().order_by('-created_at')
        }
        return render(request , template_name , ctx)

    def post(self, request):
        service = models.Service.objects.get(pk=request.POST['service'])
        sp_request = models.SparePartRequest(
            service=service,
            requested_parts=request.POST['requested_parts'],
            details=request.POST['details'],
            created_by=request.user
        )
        sp_request.save()
        messages.success(request, 'تم حفظ الطلب !')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class ConfirmSparePartRecieve(generic.View):
    def post(self, request):
        sp_request = models.SparePartRequest.objects.get(
            pk=request.POST['sp_request'])
        sp_request.status = 'recieved'
        sp_request.recievied_by = request.user
        sp_request.recievied_at = datetime.datetime.now()
        sp_request.save()

        messages.success(request, 'تم تأكيد استلام قطع الغيار ')

        return redirect(reverse_lazy('service:service_details', kwargs={'pk':  sp_request.service.id}))



# htmx views
def service_request(request):
    service_type = request.GET['type']
    if service_type == 'install':
        template = 'service/partials/install.html'
    elif service_type == 'repair':
        template = 'service/partials/repair.html'
    ctx = {
        'companies': User.objects.filter(role='company')
    }
    return render(request, template, ctx)


def render_service_data(request):
    '''
    Using HTMX to  return specific filtered service and patial dom elements 
    '''
    base_temp_name = 'service/partials/htmx/'
    service = request.GET['service']
    data = request.GET['data']
    templates = {
        ('install', 'all'): base_temp_name + 'all.html',
        ('install', 'new'): base_temp_name + 'new_services.html',
        ('install', 'under_process'): base_temp_name + 'under_process.html',
        ('install', 'upcoming_appoints'): base_temp_name + 'upcoming_appointments.html',
        ('install', 'late_services'): base_temp_name + 'late_services.html',
        ('install', 'on_hold'): base_temp_name + 'on_hold.html',
        ('install', 'new_favourite'): base_temp_name + 'favs.html',
        ('install', 'processing_favourite'): base_temp_name + 'favs.html',
        ('repair', 'all'): base_temp_name + 'all.html',
        ('repair', 'new'): base_temp_name + 'new_services.html',
        ('repair', 'under_process'): base_temp_name + 'under_process.html',
        ('repair', 'upcoming_appoints'): base_temp_name + 'upcoming_appointments.html',
        ('repair', 'late_services'): base_temp_name + 'late_services.html',
        ('repair', 'on_hold'): base_temp_name + 'on_hold.html',
        ('repair', 'spare_parts'): base_temp_name + 'spare_parts.html',
    }

    late_services = list(
        filter(lambda x: x.late, models.Service.objects.all()))
    late_repair_services = [
        service for service in late_services if service.service_type == 'repair']
    late_install_services = [
        service for service in late_services if service.service_type == 'install']
    ctxs = {
        ('install', 'all'): {
            'services': models.Service.objects.install().filter( archive =False )
        },
        ('install', 'upcoming_appoints'): {
            'appointments': models.Appointment.objects.upcoming_install()
        },
        ('install', 'late_services'): {
            'services': late_install_services
        },
        ('install', 'new'): {
            'services': models.Service.objects.new().filter(service_type='install' , hold = False),
            'title': 'طلبات التركيب الجديدة '
        },
        ('install', 'under_process'): {
            'services': models.Service.objects.under_process().filter(service_type='install').exclude(hold=True),
            'title': 'طلبات التركيب الجارية '
        },
        ('install', 'on_hold'): {
            'services': models.Service.objects.hold().filter(service_type='install')
        },
        ('install', 'new_favourite'): {
            'services': models.Service.objects.install().filter(favourite=True, status='new' , hold = False),
            'title': 'مفضلات التركيب الجديدة '
        },
        ('install', 'processing_favourite'): {
            'services': models.Service.objects.install().filter(favourite=True, status='under_process'),
            'title': 'مفضلات التركيب جاري تنفيذها  '
        },
        ('repair', 'all'): {
            'services': models.Service.objects.repair().filter( archive =False )} ,
        ('repair', 'upcoming_appoints'): {
            'appointments': models.Appointment.objects.upcoming_repair()
        },
        ('repair', 'new'): {
            'services': models.Service.objects.new().filter(service_type='repair' , hold = False),
            'title': 'طلبات الصيانة الجديدة '
        },
        ('repair', 'under_process'): {
            'services': models.Service.objects.under_process().filter(service_type='repair', hold = False),
            'title': 'طلبات الصيانة الجارية '
        },
        ('repair', 'late_services'): {
            'services': late_repair_services
        },
        ('repair', 'on_hold'): {
            'services': models.Service.objects.hold().filter(service_type='repair')
        },
        ('repair', 'spare_parts'): {
            'services': models.SparePartRequest.objects.filter(service__service_type='repair')
        },

    }

    template = templates.get((service, data), '')
    ctx = ctxs.get((service, data), {})

    return render(request, template, ctx)
