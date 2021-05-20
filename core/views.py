from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from operator import attrgetter
from itertools import chain
from django.shortcuts import render
from accounts.models import User
from django.contrib import messages
from service.models import Service_request
from quarter.models import Quarter_service
from core.models import Task
from django.http import HttpResponseRedirect
from .models import Customer
# Create your views here.


def index(request):

    new_requests = Service_request.objects.new()
    under_process = Service_request.objects.under_process()
    done = Service_request.objects.done()

    tecnicians = User.objects.all().filter(role=3)
    ctx = {

        'new_request': new_requests,
        'under_process': under_process,
        'done': done,
        'technicians': tecnicians}
    return render(request, 'index.html', ctx)


def dashboard(request):

    # all  requests
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
    repair_under_process = Service_request.objects.repair().exclude(status="closed")
    install_under_process = Service_request.objects.install().exclude(status="closed")

    ########################################################### NEED TO CHANGE LATER ###########
    quarter_under_process = Quarter_service.objects.all()
    ###############################
    # All under process
    all_under_process = sorted(
        chain(repair_under_process, install_under_process, quarter_under_process),
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


def all_users(request):
    all_users = User.objects.all().order_by('role')
    sales = User.objects.all().filter(role=4)
    tech = User.objects.all().filter(role=3)

    ctx = {
        "all_users": all_users,
        "sales": sales,
        "tech": tech
    }
    return render(request, "core/users.html", ctx)


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
