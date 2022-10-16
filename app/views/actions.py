from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import reverse

from app.models import Registration, Attendee
from app.models import Profile

from users.models import CustomUser



@login_required
def profile_go_action(request,pk):

    admin_user = CustomUser.objects.get(pk=1)

    profile = get_object_or_404(Profile, pk=pk)

    if request.user == admin_user:

        # first make sure there are no other profiles set to the Admin User
        admin_user_profiles = Profile.objects.filter(
            user = admin_user
        ).update(user=None)

        # if a user is currently set and its not admin
        # set a temp user id and set user to admin_user
        if profile.user and profile.user != admin_user:

            profile.temp_user_id = profile.user.id
            profile.user = admin_user
            profile.save()

        # if there is no user, set it to the admin user
        else:

            profile.user = admin_user
            profile.save()

        #then redirect to the account
        return HttpResponseRedirect(
            reverse('account:profile-home', args=(profile.uuid,)))

    else:
        return HttpResponse('Not Authorized User')
