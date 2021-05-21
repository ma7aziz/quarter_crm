from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import User, Section, Qouta
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from service.models import Service_request, Appointment
from quarter.models import Quarter_service
from operator import attrgetter
from itertools import chain
from core.models import Task
# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def create_user(request):
    if request.method == "POST":
        username = request.POST['username']
        name = request.POST['name']
        phone = request.POST['phone']
        role = request.POST['role']
        favourite_count = request.POST['favourite_count']

        if request.POST['password1'] == request.POST['password2']:
            user = User(username=username, name=name,
                        phone=phone, role=role)
            user.set_password(request.POST['password1'])
            if request.FILES:
                user.files = request.FILES['attach_file']
            user.save()
            qouta = Qouta(user=user, max_requests=favourite_count)
            qouta.save()
            user.favourite_qouta = qouta
            user.save()

            messages.success(request, "تم انشاء حساب المستخدم")
        else:
            messages.error(request,
                           "كلمة السر غير متطابقة .. برجا المحاولة مرة اخري ")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_user(request):
    user = User.objects.get(pk=request.POST['user_id'])
    user.name = request.POST['name']
    user.username = request.POST['username']
    user.phone = request.POST['phone']
    user.email = request.POST['email']
    user.role = request.POST['role']
    if request.POST.get('section'):
        for s in request.POST.getlist('section'):
            sect = Section.objects.get(pk=s)
            user.section.add(sect)
    if request.FILES.get('attach_file'):
        user.files = request.FILES['attach_file']
    user.save()
    messages.success(request, "تم تعديل البيانات بنجاح ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "أهلا بك مرة اخري ")
            if user.role == 1:  # admin
                return HttpResponseRedirect('/')
            elif user.role == 2:  # install mng
                return HttpResponseRedirect('/install')
            elif user.role == 3:  # repair mng
                return HttpResponseRedirect('/repair')
            elif user.role == 8:  # tech
                return HttpResponseRedirect('/new_tasks')
            else:  # quarter Staff
                return HttpResponseRedirect('quarter')

        else:

            messages.error(
                request, 'username or password not correct')
            print(messages)
            return redirect('login')
    else:
        return render(request, 'login.html')


def profile(request, username):
    user = User.objects.get(username=username)
    submitted_orders = Service_request.objects.all().filter(created_by=user)
    submitted_quarter_orders = Quarter_service.objects.all().filter(created_by=user)
    all_submitted = sorted(chain(
        submitted_orders, submitted_quarter_orders), key=attrgetter('timestamp'), reverse=True)
    completed_tasks = []
    current_tasks = []
    if user.role == 3:
        completed_tasks = sorted(chain(Appointment.objects.all().filter(
            technician=user).filter(status="closed"), Task.objects.all().filter(employee=user).exclude(status="open")), key=attrgetter("timestamp"))
        current_tasks = Appointment.objects.all().filter(
            technician=user).filter(status="open")
    other_tasks = Task.objects.open().filter(employee=user).order_by("due_date")

    ctx = {
        'user': user,
        'submitted_orders': submitted_orders,
        'submitted_quarter_orders': submitted_quarter_orders,
        'all_submitted': all_submitted,
        'completed_tasks': completed_tasks,
        'current_tasks': current_tasks,
        'other_tasks': other_tasks,
        'other_completed': Task.objects.all().filter(employee=user).exclude(status="open")
    }
    return render(request, 'registration/profile.html', ctx)


def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()

    messages.success(request, "تم حدف المستخدم !")
    return redirect('dashboard')


# custome  users views
def new_tasks(request):
    if request.user.role == 8:
        requests = Appointment.objects.filter(
            status="open", technician=request.user).order_by('date')
    other_tasks = Task.objects.open().filter(employee=request.user)

    return render(request, 'repair/index.html', {'requests': requests, 'other_tasks': other_tasks})


def history(request):
    if request.user.role == 8:
        requests = Appointment.objects.filter(
            technician=request.user).exclude(status="open")
    other_tasks = Task.objects.filter(
        employee=request.user).exclude(status="open")
    return render(request, 'repair/index.html', {'requests': requests, 'other_tasks': other_tasks})


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, '!تم تغيير كلمة السر بنجاح ')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def edit_qouta(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['user_id'])
        user.favourite_qouta.max_requests = request.POST['max_number']
        user.favourite_qouta.save()
        messages.success(
            request, '!تم التعديل ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
