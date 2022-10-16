from django.core.exceptions import PermissionDenied
from app.models import Profile

def view_login_required(function):

    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated \
            and request.user.groups.filter(name='appview').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap

def edit_login_required(function):

    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated and \
            request.user.groups.filter(name='appedit').exists():

            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
