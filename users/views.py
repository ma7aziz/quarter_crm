from typing import Any, Dict
from django.shortcuts import render , redirect
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from .models import User
from .forms import CreateUserForm
from django.http import JsonResponse , HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from .choices import USER_ROLES
from core.decorators import allowed_roles
from django.utils.decorators import method_decorator
# Create your views here.
##login 
##create user 
##edit user 
@method_decorator(allowed_roles(['admin' , 'install_supervisor' ]) ,name='dispatch')
class UserList(PermissionRequiredMixin  , generic.ListView ):
    '''
    List all sytsem users 
    '''
    permission_required = 'user.view_user'
    model = User
    template_name = 'authentication/user_list.html'
    context_object_name = 'users'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        print(super().get_context_data(**kwargs))
        return super().get_context_data(**kwargs)
    
class UserDetails(generic.DetailView , PermissionRequiredMixin):
    '''
    specific user details 
    '''
    model = User
    permission_required = 'users.view_user'
    template_name = 'authentication/user_details.html'
    lookup_field = 'id'
    context_object_name = 'user'
    
    
    def get_context_data(self, **kwargs):
        kwargs['user_roles'] = USER_ROLES
        return super().get_context_data(**kwargs)
    

class Login(LoginView):
    template_name = "authentication/login.html"
    def form_invalid(self, form):
        '''
        override error message when invalid login credintials 
        '''
        form.errors['__all__'][0] = 'يرجي التأكد من اسم المستخدم وكلمة المرور !!'
        return super().form_invalid(form)

@method_decorator(allowed_roles(['admin' , 'install_supervisor' ]) ,name='dispatch')
class CreateUser(generic.View ):
    template_name = 'authentication/create_user.html'
    def get(self , request , *args , **kwargs ):
        ctx = {
            'form' : CreateUserForm(user_role=request.user.role)
        }
        return render(request , self.template_name , ctx)
    
    def post(self , request):
        form  = CreateUserForm(request.POST )
        
        if form.is_valid():
            user = form.save()
            messages.success(request , 'تم أضافة مستخدم جديد !')
            
        else :
            return render(request , self.template_name , {'form' : CreateUserForm()} )
        return redirect(reverse_lazy('users:user_list'))
        
    
    
class DeleteUser(PermissionRequiredMixin , generic.DeleteView ):
    permission_required = 'user.delete_user'
    model = User
    lookup_field = 'id'
    success_url = reverse_lazy('users:user_list')
    
class EditUserDetails( generic.View):
    '''
    Edit user data /name, username, phone , role , favorite qouta 
    '''
    def post(self , request):
        try : 
            user = User.objects.get(pk = request.POST['user'])
            user.name = request.POST['name']
            user.username = request.POST['username']
            user.phone_number = request.POST['phone_number']
            user.role = request.POST['role'] 
            user.favourite_qouta = request.POST['favourite_qouta']
            
            user.install = bool(request.POST.get('install', False))
            user.repair = bool(request.POST.get('repair', False))
            user.quarter = bool(request.POST.get('quarter', False))
            user.save()
            messages.success(request , 'تم تحديث بيانات المستخدم !')
            
        except Exception as e :
            messages.error(request , f'خطأ .. {e}')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    

class ChangeUserPassword(generic.View):
    def post(self , request):
        try : 
            user = User.objects.get(pk = request.POST['user'])
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 == password2 :
                user.set_password(password1)
                user.save()
            else: 
                messages.error(request , 'رمز المرور غير متطابق !! ')
            messages.success(request , 'تم تحديث بيانات المستخدم !')
        except Exception as e: 
            messages.error(request , f'خطأ .. {e}')
            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
    
# username validateion 
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
            'is_taken': User.objects.filter(username=username).exists()
        }
    return JsonResponse(data)