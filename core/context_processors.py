
from users.models import User

def context(request):
    ctx = {}
    if request.user.is_authenticated : 
        if  request.user.role == 'company':
            companies = User.objects.all().filter(id = request.user.id)
        else :
            companies =  User.objects.filter(role='company')
        ctx = {
            'companies': companies
        }
    
    return ctx