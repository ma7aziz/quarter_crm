
from users.models import User

def context(request):
    ctx = {}
    if request.user.is_authenticated : 
        if  request.user.role == 'company':
            companies = request.user
        else :
            companies =  User.objects.filter(role='company')
        ctx = {
            'companies': companies
        }
    
    return ctx