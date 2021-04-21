from django.shortcuts import render, redirect
from .models import User, Section
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from service.models import Service_request, Appointment
from quarter.models import Quarter_service
from operator import attrgetter
from itertools import chain
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
        # file = request.FILES['attach_file']
        if request.POST['password1'] == request.POST['password2']:
            user = User(username=username, name=name,
                        phone=phone, role=role)
            user.set_password(request.POST['password1'])
            user.save()
            for s in request.POST.getlist('section'):
                sect = Section.objects.get(pk=s)
                user.section.add(sect)
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
    for s in request.POST.getlist('section'):
        sect = Section.objects.get(pk=s)
        user.section.add(sect)
    user.save()
    messages.success(request, "تم تعديل البيانات بنجاح ")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.role == 1:
                    return HttpResponseRedirect('/')
                elif user.role == 4 or user.role == 3:
                    return HttpResponseRedirect('repair/')
                elif user.role == 6:
                    return HttpResponseRedirect('quarter')
        else:
            print('user is none')
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
        completed_tasks = Appointment.objects.all().filter(
            technician=user).filter(status="closed")
        current_tasks = Appointment.objects.all().filter(
            technician=user).filter(status="open")
    ctx = {
        'user': user,
        'submitted_orders': submitted_orders,
        'submitted_quarter_orders': submitted_quarter_orders,
        'all_submitted': all_submitted,
        'completed_tasks': completed_tasks,
        'current_tasks': current_tasks
    }
    return render(request, 'registration/profile.html', ctx)


def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()

    messages.success(request, "تم حدف المستخدم !")
    return redirect('dashboard')
