from django.shortcuts import render

from accounts.forms import UserForm
from accounts.models import User
from repair.forms import RepairRequestForm
from repair.models import Repair_request
# Create your views here.


def index(request):
    repairForm = RepairRequestForm()
    repair_requests = Repair_request.objects.all()
    tecnicians = User.objects.all().filter(role=3)
    ctx = {
        'repairForm': repairForm,
        'repair_request': repair_requests,
        'technicians': tecnicians}
    return render(request, 'index.html', ctx)
