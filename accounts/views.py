from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html', {'form': RepairRequestForm})


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
        print(user)
        if user is not None:
            print('user not none ')
            if user.is_active:
                login(request, user)
                print('user logged in ')
                if user.role == 1:
                    return HttpResponseRedirect('/')
                elif user.role == 4 or 3:
                    print(user.role)
                    return HttpResponseRedirect('repair/')
        else:
            print('user is none')
    else:
        return render(request, 'login.html')
