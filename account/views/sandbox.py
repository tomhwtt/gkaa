from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import uuid
import json
import boto3
from decouple import config

from app.models import Profile, ProfileImage, Section, OldHighlight, OriginalUser
from users.models import CustomUser

from utils.pillow import resize_image
from utils.utils import create_short_code



@login_required
def sandbox(request):

    image_set = ProfileImage.objects.exclude(
        image = ''
    )

    # set the Amazon S3 Client
    client = boto3.client('s3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
        )

    for image in image_set:

        # create a new image name
        image_name = create_short_code() + '.jpg'

        copy_source = {
            'Bucket': 'gkaa-assets',
            'Key': 'media/' + image.image
        }

        client.copy(
            copy_source,
            'gkaa-imgix',
            'images/profiles/' + image_name
        )

        # save the image name
        image.name = image_name
        image.save()

    return HttpResponse(image_set.count())


@login_required
def sandbox_create_oldhighlights(request):

    profile_list = Profile.objects.all()

    for p in profile_list:

        # add team highlights
        if p.team_highlights_old:

            h = OldHighlight(
                profile = p,
                text = p.team_highlights_old,
                type = 1
            )
            h.save()

        if p.army_highlights_old:

            h = OldHighlight(
                profile = p,
                text = p.army_highlights_old,
                type = 2
            )
            h.save()

        if p.civilian_highlights_old:

            h = OldHighlight(
                profile = p,
                text = p.civilian_highlights_old,
                type = 3
            )
            h.save()

        if p.current_status_old:

            h = OldHighlight(
                profile = p,
                text = p.current_status_old,
                type = 4
            )
            h.save()


    return HttpResponse('sandbox')

@login_required
def sandbox_create_short_code(request):

    profile_list = Profile.objects.all()

    for p in profile_list:

        unq = str(p.uuid)
        split = unq.split('-')
        short_code = split[0] + split[1]

        p.short_code = short_code

        p.save()



    return HttpResponse('sandbox')


@login_required
def sandbox_create_home_origin(request):

    profile_list = Profile.objects.exclude(hometown='')
    num_profiles = 0

    for p in profile_list:

        split = p.hometown.split(',')

        if len(split) == 2:

            city = split[0].strip()
            state = split[1].strip()

            p.home_city = city

            if len(state) == 2:
                p.home_state = state

            p.save()

    return HttpResponse(num_profiles)


@login_required
def sandbox_connect_user(request):

    # set the current user
    current_user = request.user

    user_list = CustomUser.objects.all()

    for user in user_list:

        try:

            profile = Profile.objects.get(member_id = user.profile_id)
            profile.user = user
            profile.save()

        except:
            pass

    return HttpResponse(user_list.count())


@login_required
def sandbox_originaluser_type(request):

    # loop the OriginalUsers
    original_list = OriginalUser.objects.all()

    for o in original_list:

        try:

            profile = Profile.objects.get(member_id=o.member_id)
            o.type = profile.type
            o.save()

        except:
            pass

    return HttpResponse('user type')
