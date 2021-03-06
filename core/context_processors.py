from accounts.models import Section, ROLE, User
from service.models import lateDays

def add_variable_to_context(request):
    sections = Section.objects.all()
    users = User.objects.all()
    late_days  = lateDays.objects.get(pk = 1)
    companies = users.filter(role =  11 )
    print(companies)
    ctx = {
        "sections": sections,
        'roles': ROLE,
        'users': users , 
        'days' :late_days.days,
        "companies" : companies
    }

    return ctx
