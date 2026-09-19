from functools import wraps
from django.http import HttpResponseForbidden

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_customer(user):
    return user.groups.filter(name="Customer").exists()

def role_required(*roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            user_roles = request.user.groups.values_list("name",flat=True)

            if not any(role in user_roles for role in roles):
                return HttpResponseForbidden("You do not have permission to access this resource.")

            return view_func(request,*args,**kwargs)

        return wrapper

    return decorator