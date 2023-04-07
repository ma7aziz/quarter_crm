from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

def allowed_roles(allowed_roles=[]):
    """
    Decorator to restrict access based on the user's role
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please log in to view this page')
                return redirect('login')

            if request.user.role not in allowed_roles:
                messages.warning(request, 'You are not authorized to view this page. Redirecting to home page...')
                return redirect(reverse_lazy('core:index'))

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
