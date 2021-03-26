from django.shortcuts import render
from accounts.models import User
from repair.forms import RepairRequestForm
from repair.models import Repair_request
# Create your views here.


def index(request):
    repairForm = RepairRequestForm()
    new_requests = Repair_request.objects.new()
    under_process = Repair_request.objects.under_process()
    done = Repair_request.objects.done()

    tecnicians = User.objects.all().filter(role=3)
    ctx = {
        'repairForm': repairForm,
        'new_request': new_requests,
        'under_process': under_process,
        'done': done,
        'technicians': tecnicians}
    return render(request, 'index.html', ctx)
