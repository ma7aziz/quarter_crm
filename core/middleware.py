from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import resolve

def login_exempt(view):
    view.login_exempt = True
    return view


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_view_names = settings.LOGIN_EXEMPT_URLS

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, 'login_exempt', False):
            return

        if request.user.is_authenticated:
            return

        view_name = resolve(request.path).view_name
        if view_name in self.exempt_view_names:
            return

        return login_required(view_func)(request, *view_args, **view_kwargs)
    
    
