from operator import attrgetter
from itertools import chain
from django.shortcuts import render
from accounts.models import User

from service.models import Service_request
from quarter.models import Quarter_service
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


def dashboard(request):
    # all requests count
    # all new process count

    # under_process
    repair_under_process = Service_request.objects.repair().exclude(status="closed")
    install_under_process = Service_request.objects.install().exclude(status="closed")

    ########################################################### NEED TO CHANGE LATER ###########
    quarter_under_process = Quarter_service.objects.all()
    print(quarter_under_process.count())
    ###############################
    # All under process
    all_under_process = sorted(
        chain(repair_under_process, install_under_process, quarter_under_process),
        key=attrgetter('timestamp'), reverse=True)

    # all done count
    # all users
    users = User.objects.all().order_by("role")[:10]
    ctx = {
        'users': users,
        ## under process requests ##
        "all_cur": all_under_process,
        'repair_cur': repair_under_process,
        'install_cur': install_under_process,
        'quarter_cur': quarter_under_process
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
