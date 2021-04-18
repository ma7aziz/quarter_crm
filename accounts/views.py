from django.shortcuts import render
from .models import User, Section
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


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
