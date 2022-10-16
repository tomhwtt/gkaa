from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
import datetime
from django.contrib.auth.decorators import login_required

import boto3
from decouple import config

from app.models import OriginalUser, OldProfile, Profile, TeamDate, OfTheYear, Registration, Attendee, Gallery, OldGalleryImage, GalleryImage, OldHighlight,ProfileImage, Event, ProfileEntry, EntryType

from users.models import CustomUser

from random import randrange, shuffle
import uuid
import datetime
import requests
import json
import math

from django.core.mail import send_mail
from utils.postmark import send_contactrequest_email, send_schedule_email
from utils.utils import create_short_code

# temp for Sandbox Code
from app.models import EventRegistration
from utils.postmark import send_eventregistration_email


def sandbox_email_everyone(request):

    event = Event.objects.get(short_code='reunion-2021')

    reg_list = event.eventregistration_set.filter(
        emailed = False
    )[:20]

    email_list = []
    total_emails = 0

    for reg in reg_list:

        if not reg.emailed and reg.email not in email_list:

            email_list.append(reg.email)

            # then update all registrations with this email
            update = EventRegistration.objects.filter(
                email = reg.email
            ).update(
                emailed = True
            )

            send_eventregistration_email(reg)

            total_emails += 1


    return HttpResponse(total_emails)

# removes registrations with no subevents
@login_required
def sandbox(request):

    event = Event.objects.get(pk=2)
    cutoff = datetime.datetime.now() - datetime.timedelta(hours=3)

    num_empty = 0

    registration_list = event.eventregistration_set.filter(
        stripe_charge_id = '',
        date__lt = cutoff
    )

    return_name = event.name + ' | ' + str(registration_list.count())

    for reg in registration_list:
        reg.delete()

    return HttpResponse(return_name)

def sandbox_teamdate(request):

    profile_set = Profile.objects.all()

    for profile in profile_set:

        # set the teamdate set
        teamdate_set = profile.teamdate_set.all()

        # set the profile dates array
        teamdate_string = ''

        for d, date in enumerate(teamdate_set):

            # add the start year
            teamdate_string += str(date.start_year)

            # add the end year if there is one
            if date.end_year:
                teamdate_string += '-' + str(date.end_year)

            # if this is not the last record, add a comma
            if d != profile.teamdate_set.count()-1:
                teamdate_string += ','

        profile.teamdate_string = teamdate_string
        profile.save()



    return HttpResponse('sandbox')

@login_required
def sandbox_year(request):

    year = int('1960')

    profile_list = Profile.objects.filter(
        teamdate__start_year__lte = year,
        teamdate__end_year__gte = year,
        do_not_display = False,
        type = 1 # alumnus
        ).order_by('last_name')

    context = {
        'profile_list': profile_list
    }

    return render(request, 'app/sandbox/search.html', context)

@login_required
def sandbox_set_update_priority(request):

    num_priority = 0

    profile_list = Profile.objects.filter(
        type = 1
    )

    for profile in profile_list:

        priority = 0

        start_year = profile.start_year()

        if start_year and int(start_year) < 1971:
            priority += 3
        elif start_year and int(start_year) > 1970 and int(start_year) < 1986:
            priority += 2
        elif start_year and int(start_year) > 1985 and int(start_year) < 2000:
            priority += 1

        if profile.oldhighlight_set.count():
            priority += profile.oldhighlight_set.count()


        profile.update_priority = priority
        profile.save()


    return HttpResponse('priority')

@login_required
def sandbox_set_oldhighlights(request):

    profile_list = Profile.objects.filter(
        old_highlights = False
    )

    for profile in profile_list:

        op = OldProfile.objects.get(
            member_id = profile.member_id
        )

        if op.army_jobs:

            h = OldHighlight(
                profile = profile,
                title = 'Army Jobs',
                text = op.army_jobs,
                slug = 'army-jobs'
            )

            h.save()

        if op.team_jobs:

            h = OldHighlight(
                profile = profile,
                title = 'Team Jobs',
                text = op.team_jobs,
                slug = 'team-jobs'
            )

            h.save()

        if op.army_beats:

            h = OldHighlight(
                profile = profile,
                title = 'Beat This (Army)',
                text = op.army_beats,
                slug = 'army-beats'
            )

            h.save()

        if op.civilian_beats:

            h = OldHighlight(
                profile = profile,
                title = 'Beat This (Civilian)',
                text = op.civilian_beats,
                slug = 'civilian-beats'
            )

            h.save()

        if op.team_beats:

            h = OldHighlight(
                profile = profile,
                title = 'Beat This (Team)',
                text = op.team_beats,
                slug = 'team-beats'
            )

            h.save()

        if op.awards:

            h = OldHighlight(
                profile = profile,
                title = 'Awards',
                text = op.awards,
                slug = 'awards'
            )

            h.save()

        if op.comments:

            h = OldHighlight(
                profile = profile,
                title = 'Comments',
                text = op.comments,
                slug = 'comments'
            )

            h.save()

        if op.current_status:

            h = OldHighlight(
                profile = profile,
                title = 'Current Status',
                text = op.current_status,
                slug = 'current-status'
            )

            h.save()

        profile.old_highlights = True
        profile.save()


    return HttpResponse('sandbox')


@login_required
def sandbox_registration_name(request):

    registration_list = Registration.objects.all()

    for r in registration_list:

        name_list = r.name.strip().split(' ')

        if len(name_list) == 2:

            first_name = name_list[0].strip()
            last_name = name_list[1].strip()

            r.first_name = first_name
            r.last_name = last_name
            r.save()

    return HttpResponse('updated')

@login_required
def sandbox_attendees(request):

    friday_attendees = 0
    saturday_attendees = 0

    # get attendees where the Registration stripe_charge_id is not blank
    attendee_list = Attendee.objects.exclude(
        registration__stripe_charge_id='')

    for a in attendee_list:

        if a.event == 1:
            friday_attendees += 1

        if a.event == 2:
            saturday_attendees += 1

    return HttpResponse('Friday: ' + str(friday_attendees) + ' | Saturday: ' + str(saturday_attendees))


@login_required
def sandbox_email(request):


    mail = send_mail(
            'You email subject',
            'Super awesome email content.',
            'gkaa@goldenknightsalumni.org',
            ['tomhwtt@gmail.com'],
            fail_silently=False
            )


    return HttpResponse(mail)


@login_required
def sandbox_search_field(request):

    profile_list = Profile.objects.all()

    for profile in profile_list:

        search_field = ''

        search_field += profile.first_name + ' '
        search_field += profile.last_name + ' '
        search_field += profile.nickname + ' '
        search_field += profile.aka

        profile.search_field = search_field
        profile.save()

    return HttpResponse('set search field')

@login_required
def sandbox_strip_names(request):

    profile_list = Profile.objects.all()

    for profile in profile_list:

        cleaned_first_name = profile.first_name.strip()
        cleaned_last_name = profile.last_name.strip()

        profile.first_name = cleaned_first_name
        profile.last_name = cleaned_last_name

        profile.save()

    return HttpResponse('strip names')


@login_required
def sandbox_highlight_sort_order(request):

    profile_list = Profile.objects.all()

    for profile in profile_list:

        for index, highlight in enumerate(profile.highlight_set.all()):

            highlight.sort_order = index
            highlight.save()

    return HttpResponse('set sort order')


# transfer images from OldGalleryImage to GalleryImage
@login_required
def sandbox_gallery_transfer(request):

    old_gallery = OldGalleryImage.objects.filter(transferred=False)

    for o in old_gallery:

        # set the gallery
        gallery = Gallery.objects.get(id=o.gallery)

        # set the image path
        image = 'gallery/' + o.old_id + '-lg.jpg'

        if o.year != '':
            year = o.year
        else:
            year = None

        galleryimage = GalleryImage(
            gallery = gallery,
            caption = o.caption,
            credit = o.credit,
            year = year,
            image = image,
            uuid = uuid.uuid4(),
            old_id = o.old_id
        )

        galleryimage.save()

        # check to see if the image exists
        image_exists = galleryimage.image.storage.exists(galleryimage.image.name)

        # then update the GalleryImage
        galleryimage.image_exists = image_exists
        galleryimage.save()

        # mark the original as transferred
        o.transferred = True
        o.save()

    return HttpResponse(str(old_gallery.count()) + ' transferred')

@login_required
def sandbox_galleryimage_exists(request):

    galleryimage_list = GalleryImage.objects.filter(image_exists=False)

    for galleryimage in galleryimage_list:

        # check to see if the image exists
        image_exists = galleryimage.image.storage.exists(galleryimage.image.name)

        if image_exists:
            galleryimage.image_exists = image_exists
            galleryimage.save()

    return HttpResponse('gallery image exists')
