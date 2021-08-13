
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from operator import attrgetter
from itertools import chain
from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from service.models import Service_request
from quarter.models import Quarter_service
from core.models import Task
from django.http import HttpResponseRedirect
from .models import Customer
from service.utils import check_qouta, get_data
# Create your views here.


@login_required
def index(request):
    if request.user.is_authenticated:
        check_qouta(request.user.id)
        if request.user.role == 1:  # Admin
            return render(request, 'index.html')
        elif request.user.role == 5 or request.user.role == 10:
            ####sale##
            return redirect("sales_view")
        elif request.user.role == 8:  # technician
            return redirect("new_tasks")
        elif request.user.role == 2:  # install mngr
            return redirect("install_index")
        elif request.user.role == 3:  # repair mngr
            return redirect("repair_index")

        else:
            # quarter staff
            return redirect("quarter_index")

    return render(request, 'index.html')


@login_required
def dashboard(request):
    if request.user.role == 1:
        # get_data()
        repair_requests = Service_request.objects.repair()
        install_requests = Service_request.objects.install()
        quarter_requests = Quarter_service.objects.all()
        all_requests = sorted(
            chain(repair_requests, install_requests, quarter_requests), key=attrgetter('timestamp'), reverse=True)

        # ON HOLD
        quarter_hold = Quarter_service.objects.on_hold()
        service_hold = Service_request.objects.on_hold()

        all_on_hold = sorted(chain(quarter_hold, service_hold),
                             key=attrgetter('timestamp'), reverse=True)

        # under_process
        repair_under_process = Service_request.objects.repair().exclude(
            status="closed").exclude(status="done")
        install_under_process = Service_request.objects.install().exclude(
            status="closed").exclude(status="done")

        ########################################################### NEED TO CHANGE LATER ###########
        quarter_under_process = Quarter_service.objects.all()
        ###############################
        # All under process
        all_under_process = sorted(
            chain(repair_under_process, install_under_process,
                  quarter_under_process),
            key=attrgetter('timestamp'), reverse=True)

        # NEW REQUESTS
        new_repair = Service_request.objects.repair().filter(status="new")
        new_install = Service_request.objects.install().filter(status="new")
        new_quarter = Quarter_service.objects.all().filter(status=1)
        all_new = sorted(
            chain(new_repair, new_install, new_quarter), key=attrgetter('timestamp'), reverse=True
        )
        # special tasks
        tasks = Task.objects.all()
        current_tasks = Task.objects.all().exclude(status="closed")
        active_tasks = Task.objects.all().filter(status="open")
        completed_tasks = Task.objects.all().filter(status="completed")

        users = User.objects.all().order_by("role")

        ctx = {
            "all_users": users,
            'users': users[:10],
            # all requests
            "quarter_requests": quarter_requests,
            "repair_requests": repair_requests,
            "install_requests": install_requests,
            "all_requests": all_requests,
            # ON HOLD
            'quarter_hold': quarter_hold,
            'service_hold': service_hold,
            'all_on_hold': all_on_hold,
            ## under process requests ##
            "all_cur": all_under_process,
            'repair_cur': repair_under_process,
            'install_cur': install_under_process,
            'quarter_cur': quarter_under_process,
            # NEW REQUESTS
            "all_new": all_new,
            "new_install": new_install,
            "new_repair": new_repair,
            "new_quarter": new_quarter,
            # TASKS
            "tasks": current_tasks,
            "active_tasks": active_tasks,
            "completed_tasks": completed_tasks

        }
        return render(request, 'core/dashboard.html', ctx)
    else:
        messages.error(request, "لا يمكنك الوصول لهذة الصفحة ")
        return redirect('index')


def all_users(request):
    if request.user.role == 1:
        all_users = User.objects.all().order_by('role')
        sales = User.objects.all().filter(role=4)
        tech = User.objects.all().filter(role=3)

        ctx = {
            "all_users": all_users,
            "sales": sales,
            "tech": tech
        }
        return render(request, "core/users.html", ctx)
    else:
        messages.error(request, "لا يمكنك الوصول لهذة الصفحة ")
        return redirect('index')


def create_task(request):
    task = Task(title=request.POST["title"], due_date=request.POST['due_date'],
                created_by=request.user, employee=User.objects.get(pk=request.POST["employee"]), details=request.POST['details'])
    task.save()
    if request.FILES:
        task.files = request.FILES['files']
        task.save()
    messages.success(request, "تم ارسال المهمة ! ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_task(request):
    task = Task.objects.get(pk=request.POST['task_id'])
    if task.status == "open":
        task.status = "completed"
        task.save()
        messages.success(request, "اتمام المهمة بنجاح ")
    elif task.status == "completed":
        task.status = "closed"
        task.save()
        messages.success(request, "تم اغلاق المهمة بنجاح !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.error(request, " تم حذف المهمة ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def customers(request):
    customers = Customer.objects.all()
    paginator = Paginator(customers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = customers.count()

    return render(request, 'core/customers_data.html', {'page_obj': page_obj, })


def customer_details(request, id):
    customer = Customer.objects.get(pk=id)
    quarter_orders = Quarter_service.objects.all().filter(customer=customer)
    service_requests = Service_request.objects.all().filter(customer=customer)
    orders = sorted(
        chain(quarter_orders, service_requests), key=attrgetter('timestamp'), reverse=True
    )

    ctx = {
        "customer": customer,
        "quarter_orders": quarter_orders,
        "service_requests": service_requests,
        "orders": orders
    }

    return render(request, "core/customer_details.html", ctx)


def search(request):
    keyword = request.GET.get('s').strip()
    quarter_result = Quarter_service.objects.filter(Q(name__icontains=keyword) | Q(phone__icontains=keyword) | Q(
        notes__icontains=keyword) | Q(request_number__iexact=keyword))
    service_result = Service_request.objects.filter(Q(customer_name__icontains=keyword) | Q(phone__icontains=keyword) | Q(
        notes__icontains=keyword) | Q(request_number__iexact=keyword))
    customer_result = Customer.objects.filter(
        Q(name__icontains=keyword) | Q(phone__icontains=keyword))
    user_result = User.objects.filter(
        Q(name__icontains=keyword) | Q(phone__icontains=keyword))

    result = list(chain(quarter_result, service_result,
                        customer_result, user_result))

    ctx = {
        'results': result,
        'quarter_result': quarter_result,
        'service_result': service_result,
        'customer_result': customer_result,
        'user_result': user_result,
        'keyword': keyword
    }

    return render(request, 'core/search_results.html', ctx)


def sales_view(request):
    if request.user.role == 10:  # QUARTER SALES VIEW
        current_assigned_requests = Quarter_service.objects.all().filter(
            sales=request.user).exclude(status=15).exclude(status=13)
        quarter_current = Quarter_service.objects.all().filter(
            created_by=request.user).order_by('-timestamp').exclude(status=15).exclude(status=13)
        all_current_requests = sorted(chain(current_assigned_requests, quarter_current), key=attrgetter(
            'timestamp'), reverse=True)

        all_requests = sorted(chain(Quarter_service.objects.all().filter(
            created_by=request.user).order_by('-timestamp'), Quarter_service.objects.all().filter(
            sales=request.user)), key=attrgetter(
            'timestamp'), reverse=True)
        ctx = {
            "assigned_requests": current_assigned_requests,
            "quarter_history": quarter_current,
            "all_current_requests": all_current_requests,
            "all_requests": all_requests
        }
    else:
        check_qouta(request.user.id)
        service_history = Service_request.objects.all().filter(
            created_by=request.user).order_by('-favourite', '-timestamp')
        quarter_history = Quarter_service.objects.all().filter(
            created_by=request.user).order_by('-favourite', '-timestamp')

        all_history = sorted(chain(service_history, quarter_history),
                             key=attrgetter('favourite', 'timestamp'), reverse=True)
        # Current
        current_services = Service_request.objects.all().filter(created_by=request.user).order_by(
            '-favourite', '-timestamp').exclude(status="done").exclude(status="closed").exclude(status="new")
        current_quarter = Quarter_service.objects.all().filter(created_by=request.user).order_by(
            '-favourite', '-timestamp').exclude(status=13).exclude(status=15).exclude(status=1)
        all_current = sorted(chain(current_services, current_quarter),
                             key=attrgetter('favourite', 'timestamp'), reverse=True)
        # favorits
        favorites = Service_request.objects.all().filter(
            created_by=request.user).filter(favourite=True).order_by('-timestamp')
        ctx = {
            "service_history": service_history,
            "quarter_history": quarter_history,
            "all_history": all_history,
            # Current
            "current_services": current_services,
            "current_quarter": current_quarter,
            "all_current": all_current,
            # Favorites
            "favs": favorites
        }
    return render(request, "core/sales_view.html", ctx)


def chart(request):
    if request.is_ajax():
        repair_count = Service_request.objects.repair().count()
        install_count = Service_request.objects.install().count()
        quarter_count = Quarter_service.objects.all().count()
        labels = ['الصيانة', "التركيب ", 'كوارتر ']
        data = [repair_count, install_count, quarter_count]
        colors = ['rgba(0, 63, 92, 0.7)', 'rgba(255, 166, 0, 0.7)',
                  'rgba(239, 86, 117, 0.7)']

        return JsonResponse(data={
            'labels': labels,
            'data': data,
            'colors':  colors
        })
    return render(request, "charts.html")


def current_requests(request):
    if request.is_ajax():
        repair_under_process = Service_request.objects.repair().exclude(
            status="closed").exclude(active=False)
        install_under_process = Service_request.objects.install().exclude(
            status="closed").exclude(active=False)
        quarter_under_process = Quarter_service.objects.all().exclude(
            status=13).exclude(active=False)

        labels = ['الصيانة', "التركيب ", 'كوارتر ']
        data = [repair_under_process.count(), install_under_process.count(),
                quarter_under_process.count()]
        colors = ['rgba(0, 63, 92, 0.7)', 'rgba(255, 166, 0, 0.7)',
                  'rgba(239, 86, 117, 0.7)']

        return JsonResponse(data={
            'labels': labels,
            'data': data,
            'colors':  colors
        })
# ===============================================================================
############################# CUSTOME ERROR PAGES , 404 , 500 ###################


# def handle_404(request, exception):
#     messages.error(
#         request, "عنوان الصفحة المطلوبة غير صحيح .. برجاء المحاولة مرة اخري ! ")
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def handle_500(request, exception):
#     messages.error(request, "حدث خطأ  ما .. برجاة المحاولة مرة اخري !")
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
