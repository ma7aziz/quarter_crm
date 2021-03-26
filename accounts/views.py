from django.shortcuts import render

from repair.forms import RepairRequestForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
# Create your views here.


def index(request):
    return render(request, 'index.html', {'form': RepairRequestForm})


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
                    return HttpResponseRedirect('admin')
                elif user.role == 4:
                    print(user.role)
                    return HttpResponseRedirect('repair/')
        else:
            print('user is none')
    else:
        return render(request, 'login.html')
