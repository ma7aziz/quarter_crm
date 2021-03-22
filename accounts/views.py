from django.shortcuts import render
from .forms import UserForm
from repair.forms import RepairRequestForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {'form': RepairRequestForm})
