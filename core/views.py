from django.shortcuts import render
from accounts.models import User

from service.models import Service_request
# Create your views here.


def index(request):

    new_requests = Service_request.objects.new()
    under_process = Snew_requests = Service_request.objects.under_process()
    done = Service_request.objects.done()

    tecnicians = User.objects.all().filter(role=3)
    ctx = {

        'new_request': new_requests,
        'under_process': under_process,
        'done': done,
        'technicians': tecnicians}
    return render(request, 'index.html', ctx)
