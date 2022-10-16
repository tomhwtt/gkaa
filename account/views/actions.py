from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# python
import json
import uuid
import datetime

# third party apps
import boto3
from decouple import config
import io
from PIL import Image


from django.contrib.auth import get_user_model

from app.models import Profile, ProfileImage, OldHighlight, TeamDate, Section, OriginalUser, ProfileEntry, ProfileActivity

from users.models import CustomUser

from account.forms import ProfileForm, AccountRequestForm

from utils.utils import clean_trix_html, create_short_code, create_image_name
from utils.pillow import resize_image


# sets a ProfileImage for future deletion
@login_required
def oldhighlight_delete_action(request,pk):

    # get the current user
    current_user = request.user

    # get the profile image
    oldhighlight = get_object_or_404(OldHighlight, pk=pk)

    # set the profile
    profile = oldhighlight.profile

    # if the current user owns the profile image
    if profile.user == current_user:

        # set the date_delete to now
        oldhighlight.date_delete = datetime.datetime.now()

        # save the image
        oldhighlight.save()

        # add an activity record
        activity = ProfileActivity(
            profile = profile,
            activity = 'You deleted Previous Info',
            type = 'previous-info',
            type_id = oldhighlight.id
        )

        activity.save()

        # redirect back to images page
        return HttpResponseRedirect(reverse('account:oldhighlight-list',
            args=(profile.uuid,)))

@login_required
def oldhighlight_delete_undo_action(request,pk):

    # get the current user
    current_user = request.user

    # get the profile image
    oldhighlight = get_object_or_404(OldHighlight, pk=pk)

    # set the profile
    profile = oldhighlight.profile

    # if the current user owns the profile
    if profile.user == current_user:

        # set a date/time outside the undo timeframe
        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=30)

        # move any existing deleted images outside the undo timeframe
        recently_deleted = profile.oldhighlight_set.filter(
            date_delete__isnull = False,
            date_delete__gte = cutoff
        ).exclude(id=oldhighlight.id).update(date_delete=cutoff)

        oldhighlight.date_delete = None

        oldhighlight.save()

        # add an activity record
        activity = ProfileActivity(
            profile = profile,
            activity = 'You restored Previous Info',
            type = 'previous-info',
            type_id = oldhighlight.id
        )

        activity.save()

        # redirect back to images page
        return HttpResponseRedirect(reverse('account:oldhighlight-list',
            args=(profile.uuid,)))


# handle file uploads via Dropzone
@require_POST
@csrf_exempt
@login_required
def dropzone_action(request):

    if request.method == 'POST':

        # get the current user
        current_user = request.user

        # get the profile
        profile_id = request.POST.get('profile')
        profile = get_object_or_404(Profile, uuid=profile_id, user=current_user)

        # get the files passed in
        # this is list comprehension
        file_list = [request.FILES.get('file[%d]' % i)
            for i in range(0, len(request.FILES))]

        # for each file in the file_list
        for index, f in enumerate(file_list):

            # if there are no images yet, set this as the default profile image
            if not profile.profileimage_set.count() and index == 0:
                profile_image = True
            else:
                profile_image = False

            # save the profile image
            profileimage = ProfileImage(
                profile=profile,
                profile_image = profile_image,
                image = f
                )

            profileimage.save()

        return JsonResponse({ 'upload':'success '})

    # if not a post
    else:
        return HttpResponse('')


# delete a ProfileImage
@require_POST
@csrf_exempt
@login_required
def action_profileimage_delete(request):

    if request.is_ajax():

        # get current user
        current_user = request.user

        # set the image_uuid
        image_uuid = request.POST['image_id']

        # get the profile image
        profileimage = get_object_or_404(ProfileImage,uuid=image_uuid)

        # set the profile
        profile = profileimage.profile

        if profileimage.profile_image:
            profile_image = True
        else:
            profile_image = False

        # if the profile belongs to the current user
        # delete it from Amazon and our server
        if profile.user == current_user:

            s3_filename = 'media/' + str(profileimage.image)

            # set the boto3 client
            client = boto3.client('s3',
                aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
                )

            # delete the object
            client.delete_object(
                Bucket = 'gkaa-assets',
                Key = s3_filename
            )

            # delete from our database
            profileimage.delete()

            # if there are still images left, set the first one to the profile_image
            if profile.profileimage_set.count():

                first_image = profile.profileimage_set.first()
                first_image.profile_image = True
                first_image.save()

            return JsonResponse({'result': 'success'})

        else:

            return JsonResponse({'result': 'not-authorized'})

    # else return a blank page
    else:
        return HttpResponse('')
