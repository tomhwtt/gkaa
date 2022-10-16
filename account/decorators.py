from django.core.exceptions import PermissionDenied
from app.models import Profile

def user_owns_profile(function):

    def wrap(request, *args, **kwargs):

        profile = Profile.objects.get(uuid=kwargs['uuid'])

        if request.user.is_authenticated and profile.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
