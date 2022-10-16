from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views import generic

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from account.decorators import user_owns_profile

from decouple import config

import json
import uuid
import base64
import boto3
import datetime

from app.models import Profile, ProfileEntry, EntryType, TeamDate, ArmyDate, AccountRequest, OldHighlight, ProfileImage, EntryExample, ProfileStory

# cleaning this one up
from app.models import Section, OldProfile

from account.forms import ProfileForm, AccountRequestForm

from utils.postmark import accountrequest_notification
from utils.utils import create_short_code, update_teamdate_string, create_url_code, set_profile_show_link, create_profileupdate
from utils.boto import put_aws_object, delete_aws_object

@login_required
def account_index(request):

    # set the current user
    current_user = request.user

    if current_user.is_staff:

        profile = Profile.objects.get(user=current_user)

        context = {
            'profile': profile
        }

        return render(request, 'account/account_staff.html' ,context)

    # if user is not staff
    else:

        # try to get the Profile assigned to them
        try:
            profile = Profile.objects.get(user=current_user)

            return HttpResponseRedirect(
                reverse('account:profile-index', args=(profile.uuid,)))

        # if no profile exists, tell them to contact us
        except:

            profile = None

            context = {
                'profile': profile
            }

            return render(request, 'account/no_account.html' ,context)

@user_owns_profile
def profile_index(request,uuid):

    # get the profile if they own it
    profile = get_object_or_404(Profile, uuid=uuid)

    context = {
        'profile': profile
    }


    return render(request, 'account/profile_index.html' ,context)

@user_owns_profile
def profile_detail(request,uuid):

    # get the profile if they own it
    profile = get_object_or_404(Profile, uuid=uuid)

    # does profile have old highlights
    oldhighlight_set = profile.oldhighlights()

    # does the Profile have a profile picture
    has_profile_image = profile.profileimage_set.filter(
        profile_image = True
    ).first()


    context = {
        'profile':profile,
        'entry_list': profile.entry_list(),
        'image_set': profile.image_list(),
        'story_set': profile.profilestory_set.all(),
        'oldhighlight_set': oldhighlight_set,
        'has_profile_image': has_profile_image
    }

    return render(request, 'account/profile_detail.html' ,context)

@user_owns_profile
def profile_entries(request,uuid,type):

    profile = get_object_or_404(Profile,uuid=uuid)
    entrytype = get_object_or_404(EntryType,pk=type)

    if request.method == 'POST':

        text = request.POST['text'].strip()

        if text and len(text) < 101:

            entry = ProfileEntry(
                profile = profile,
                entrytype = entrytype,
                text = request.POST['text'].strip()
            )

            entry.save()

            set_profile_show_link(profile)

            create_profileupdate(
                profile,
                request.user,
                'add entry'
            )

            return HttpResponseRedirect(
                reverse('account:profile-entries', args=(profile.uuid,type)))

        else:
            return HttpResponseRedirect(
                reverse('account:profile-entries',
                    args=(profile.uuid,type)) + str('?e=length'))

    # if NOT POST
    else:

        entry_list = ProfileEntry.objects.filter(
            profile = profile,
            entrytype = entrytype
        )

        example_list = EntryExample.objects.filter(
            entrytype = entrytype
        )

        # entry too long error
        if request.GET.get('e') and request.GET.get('e') == 'length':
            length_error = True
        else:
            length_error = False

        context = {
            'profile': profile,
            'entry_list': entry_list,
            'example_list': example_list,
            'title': entrytype.title,
            'singular': entrytype.singular,
            'length_error': length_error
        }

        return render(request, 'account/profile_entries.html', context)

@user_owns_profile
def entry_detail(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    entry = get_object_or_404(ProfileEntry,pk=id)

    if request.method == 'POST':

        try:
            highlight = request.POST['highlight']
            entry.show_on_home = True
        except:
            entry.show_on_home = False


        entry.text = request.POST['text']
        entry.save()

        return HttpResponseRedirect(
            reverse('account:entry-detail', args=(profile.uuid,entry.id)) + str('?s=updated'))

    # if NOT POST
    else:

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        type = entry.entrytype

        if entry.show_on_home:
            checked = 'checked'
        else:
            checked = ''

        context = {
            'profile': profile,
            'entry': entry,
            'type': type,
            'update_notice': update_notice,
            'checked': checked
        }


        return render(request, 'account/entry_detail.html', context)

@user_owns_profile
def entry_delete(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    entry = get_object_or_404(ProfileEntry,pk=id)

    if request.GET.get('confirm') and request.GET.get('confirm') == 'true':

        # set entry.type before you delete entry
        type = entry.entrytype.id
        entry.delete()

        set_profile_show_link(profile)

        create_profileupdate(
            profile,
            request.user,
            'delete entry'
        )

        return HttpResponseRedirect(
            reverse('account:profile-entries', args=(profile.uuid,type)))

    else:

        context = {
            'profile': profile,
            'entry': entry,
            'type': entry.entrytype
        }

        return render(request, 'account/entry_delete.html', context)

@user_owns_profile
def profile_edit(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        form = ProfileForm(request.POST,instance=profile)

        if form.is_valid():

            profile = form.save()

            create_profileupdate(
                profile,
                request.user,
                'profile edit'
            )

            return HttpResponseRedirect(
                reverse('account:profile-edit',
                    args=(profile.uuid,)) + str('?s=updated'))

        else:
            return HttpResponse('Form is not valid')

    else:

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False


        context = {
            'profile': profile,
            'update_notice': update_notice
        }


        return render(request, 'account/profile_edit.html', context)

@user_owns_profile
def profile_dates(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        team_start_year = request.POST['team_start_year'].strip()
        team_end_year = request.POST['team_end_year'].strip()
        army_start_year = request.POST['army_start_year'].strip()
        army_end_year = request.POST['army_end_year'].strip()

        if team_start_year:

            if not team_end_year:
                team_end_year = None

            teamdate = TeamDate(
                start_year = team_start_year,
                end_year = team_end_year,
                profile = profile
            )

            teamdate.save()

            # update the teamdate_string
            update_teamdate_string(profile)

        if army_start_year:

            if not army_end_year:
                army_end_year = None

            armydate = ArmyDate(
                start_year = army_start_year,
                end_year = army_end_year,
                profile = profile
            )

            armydate.save()

        return HttpResponseRedirect(
            reverse('account:profile-dates', args=(profile.uuid,))+ str('?s=updated'))

    # if NOT POST
    else:

        teamdate_set = profile.teamdate_set.all()
        armydate_set = profile.armydate_set.all()

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'teamdate_set': teamdate_set,
            'armydate_set': armydate_set,
            'update_notice': update_notice
        }

        return render(request, 'account/profile_dates.html', context)

@user_owns_profile
def teamdate_delete(request,uuid,id):

    # get the profile
    profile = get_object_or_404(Profile,uuid=uuid)

    # get the TeamDate
    teamdate = get_object_or_404(TeamDate,pk=id)

    # delete the date
    teamdate.delete()

    # update the teamdate_string
    update_teamdate_string(profile)

    return HttpResponseRedirect(
        reverse('account:profile-dates', args=(profile.uuid,)))

@user_owns_profile
def armydate_delete(request,uuid,id):

    # get the profile
    profile = get_object_or_404(Profile,uuid=uuid)

    # get the TeamDate
    armydate = get_object_or_404(ArmyDate,pk=id)

    # delete the date
    armydate.delete()

    return HttpResponseRedirect(
        reverse('account:profile-dates', args=(profile.uuid,)))

@user_owns_profile
def oldhighlights(request,uuid):

    # get the profile
    profile = get_object_or_404(Profile, uuid=uuid)

    # get the highlight list
    oldhighlight_set = profile.oldhighlight_set.filter(
        date_delete__isnull = True
    )

    context = {
        'profile':profile,
        'oldhighlight_set': oldhighlight_set
    }

    return render(request, 'account/oldhighlights_list.html' ,context)

@user_owns_profile
def oldhighlight_delete(request,uuid,id):

    # get the profile
    profile = get_object_or_404(Profile, uuid=uuid)

    highlight = get_object_or_404(OldHighlight,pk=id)

    # we are currently just removing them from view
    # later we will create a system where they delete in X days
    highlight.date_delete = datetime.datetime.now()
    highlight.save()

    return HttpResponseRedirect(
        reverse('account:oldhighlights', args=(profile.uuid,)))

## view that manages the users Profile and roster image
@user_owns_profile
def profile_image(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        # if no file was uploaded, it will fire an error
        try:

            # set the file
            file = request.FILES['imagefile']

            # set the imageid
            image_id = request.POST['imageid']

            # the current image
            image = get_object_or_404(ProfileImage,pk=int(image_id))

            # turn off the existing profile_image or roster_image
            if image.profile_image:
                image.profile_image = False
                profile_image = True
                roster_image = False

            elif image.roster_image:
                image.roster_image = False
                roster_image = True
                profile_image = False

            image.save()

            # create a filename
            filename = create_url_code() + '.jpg'

            # upload the object to AWS
            put_aws_object(
                bucket = 'gkaa-imgix',
                key = 'images/profiles/' + filename,
                file = file
            )

            # create the new ProfileImage
            profileimage = ProfileImage(
                profile = profile,
                name = filename,
                profile_image = profile_image,
                roster_image = roster_image
            )

            profileimage.save()

            return HttpResponseRedirect(
                reverse('account:profile-image', args=(profile.uuid,)))

        # if no image is chosen, it throws an error
        except:
            return HttpResponse('Choose an Image First')

    else:

        # get the users profile_image
        profile_image = profile.profileimage_set.filter(
            profile_image = True
        ).first()

        # get the users roster_image
        roster_image = profile.profileimage_set.filter(
            roster_image = True
        ).first()


        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'profile_image': profile_image,
            'roster_image': roster_image,
            'update_notice': update_notice
        }

        return render(request, 'account/profile_image.html', context)

@user_owns_profile
def profileimage_list(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    all_images = profile.profileimage_set.all()

    profile_image = all_images.filter(
        profile_image = True
    ).first()


    roster_image = all_images.filter(
        roster_image = True
    ).first()


    image_set = all_images.filter(
        profile_image = False,
        roster_image = False
    )

    context = {
        'profile': profile,
        'image_set': image_set,
        'profile_image': profile_image,
        'roster_image': roster_image
    }

    return render(request, 'account/profileimage_list.html', context)

@user_owns_profile
def profileimage_detail(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    image = get_object_or_404(ProfileImage,pk=id)

    # show a notification after update
    if request.GET.get('s') and request.GET.get('s') == 'updated':
        notify = True
    else:
        notify = False

    if image.profile_image:
        profile_image = True
    else:
        profile_image = False

    if image.roster_image:
        roster_image = True
    else:
        roster_image = False

    button_prefix = (
        '/account/profile/' + str(profile.uuid) + '/'
    )

    # create a button list
    button_list = [
        {
            'text': 'Back to Image List',
            'color': 'btn-outline-secondary',
            'url': button_prefix + 'images'
        }
    ]

    # add the profile button
    if image.profile_image and not image.roster_image:

        url = (
            button_prefix + 'images/' + str(image.id) + '/profile/'
        )

        btn_obj = {
            'text': 'Turn off as Profile image',
            'color': 'btn-success',
            'url': url
        }

        button_list.append(btn_obj)

    elif not image.profile_image and not image.roster_image:

        url = (
            button_prefix + 'images/' + str(image.id) + '/profile/'
        )

        btn_obj = {
            'text': 'Set as Profile Image',
            'color': 'btn-outline-secondary',
            'url': url
        }

        button_list.append(btn_obj)

    if image.roster_image and not image.profile_image:

        url = (
            button_prefix + 'images/' + str(image.id) + '/roster/'
        )

        btn_obj = {
            'text': 'Turn off as Roster Image',
            'color': 'btn-success',
            'url': url
        }

        button_list.append(btn_obj)

    elif not image.roster_image and not image.profile_image:

        url = (
            button_prefix + 'images/' + str(image.id) + '/roster/'
        )

        btn_obj = {
            'text': 'Set as Roster Image',
            'color': 'btn-outline-secondary',
            'url': url
        }

        button_list.append(btn_obj)


    # put the add/edit button
    btn_obj = {
        'text': 'Add/Edit Image Details',
        'color': 'btn-outline-secondary',
        'url': button_prefix + 'images/' + str(image.id) + '/edit/'
    }

    button_list.append(btn_obj)

    btn_obj = {
        'text': 'Delete Image',
        'color': 'btn-danger',
        'url': button_prefix + 'images/' + str(image.id) + '/delete/'
    }

    button_list.append(btn_obj)


    context = {
        'profile': profile,
        'image': image,
        'profile_image': profile_image,
        'roster_image': roster_image,
        'notify': notify,
        'button_list': button_list
    }

    return render(request, 'account/profileimage_detail.html', context)

@user_owns_profile
def profileimage_edit(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    image = get_object_or_404(ProfileImage,pk=id)

    if request.method == 'POST':

        image.caption = request.POST['caption'].strip()
        image.year = request.POST['year'].strip()
        image.credit = request.POST['credit'].strip()

        image.save()

        return HttpResponseRedirect(
            reverse('account:profileimage-detail',
                args=(profile.uuid,image.id))+ str('?s=updated'))

    # if NOT POST
    else:

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        if image.profile_image:
            profile_image = True
        else:
            profile_image = False

        if image.roster_image:
            roster_image = True
        else:
            roster_image = False

        context = {
            'profile': profile,
            'image': image,
            'profile_image': profile_image,
            'roster_image': roster_image,
            'update_notice': update_notice
        }

        return render(request, 'account/profileimage_edit.html', context)

@user_owns_profile
def profileimage_new(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    # if this is a POST, we are adding a LineItemColorImage
    if request.method == 'POST':

        try:
            # set the file
            file = request.FILES['image']

            # if the file size is over 5MB
            if file.size > 5242880:

                return HttpResponse('Max File Size is 5MB')

            # if the file is not too big
            else:

                # if they clicked Add Profile Image to get to new image page
                if request.GET.get('type') and request.GET.get('type'):

                    # clear all other profile_images
                    profile.profileimage_set.filter(
                        profile_image = True
                    ).update(
                        profile_image = False
                    )

                    # set this image to True
                    profile_image = True

                # if type is not profile
                else:
                    profile_image = False

                # I can work on this (^) later
                # if type = profile, roster, etc

                profileimage = ProfileImage(
                    profile = profile,
                    name = create_url_code() + '.jpg',
                    size = file.size,
                    profile_image = profile_image
                )

                profileimage.save()

                # upload the object to AWS
                put_aws_object(
                    bucket = 'gkaa-imgix',
                    key = 'images/profiles/' + profileimage.name,
                    file = file
                )

                return HttpResponseRedirect(
                    reverse('account:profileimage-detail', args=(profile.uuid,profileimage.id)))

        except:
            return HttpResponse('No File Chosen')

    else:

        if request.GET.get('type'):
            type = request.GET.get('type').title()
        else:
            type = ''

        context = {
            'profile': profile,
            'type': type
        }

        return render(request, 'account/profileimage_new.html', context)

@user_owns_profile
def profileimage_delete(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    image = get_object_or_404(ProfileImage,pk=id)

    if request.GET.get('confirm') and request.GET.get('confirm') == 'true':

        delete_aws_object(
            bucket = 'gkaa-imgix',
            key = 'images/profiles/' + image.name
        )

        # delete the ProfileImage
        image.delete()

        return HttpResponseRedirect(
            reverse('account:profileimage-list', args=(profile.uuid,)))

    # if delete not confirmed
    else:

        context = {
            'profile': profile,
            'image': image
        }

        return render(request, 'account/profileimage_delete.html', context)

@user_owns_profile
def profileimage_profile_image(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    image = get_object_or_404(ProfileImage,pk=id)

    # reset all other images to false
    image_set = profile.profileimage_set.update(
        profile_image = False
    )

    # if it's on, turn it off
    if image.profile_image:
        image.profile_image = False

    # if it's off, turn it on
    else:
        image.profile_image = True

    # then save the image
    image.save()

    return HttpResponseRedirect(
        reverse('account:profileimage-detail',
            args=(profile.uuid,image.id)) + str('?s=updated'))

@user_owns_profile
def profileimage_roster_image(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    image = get_object_or_404(ProfileImage,pk=id)

    # reset all other images to false
    image_set = profile.profileimage_set.update(
        roster_image = False
    )

    # if it's on, turn it off
    if image.roster_image:
        image.roster_image = False

    # if it's off, turn it on
    else:
        image.roster_image = True

    # then save the image
    image.save()

    return HttpResponseRedirect(
        reverse('account:profileimage-detail',
            args=(profile.uuid,image.id)) + str('?s=updated'))

@user_owns_profile
def profile_comments(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        profile.comments = request.POST['comments']
        profile.save()

        set_profile_show_link(profile)

        return HttpResponseRedirect(
            reverse('account:profile-comments',
                args=(profile.uuid,)) + str('?s=updated'))

    else:

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'update_notice': update_notice
        }

        return render(request, 'account/comments.html', context)

@user_owns_profile
def profile_current_status(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        profile.current_status = request.POST['text']
        profile.save()

        return HttpResponseRedirect(
            reverse('account:profile-current-status',
            args=(profile.uuid,)) + str('?s=updated'))

    else:

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'update_notice': update_notice
        }

        return render(request, 'account/current_status.html', context)

@user_owns_profile
def profilestory_list(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    story_set = profile.profilestory_set.all()

    context = {
        'profile': profile,
        'story_set': story_set
    }

    return render(request, 'account/profilestory_list.html', context)

@user_owns_profile
def profilestory_detail(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.method == 'POST':

        title = request.POST['title'].strip()
        text = request.POST['text']

        story.title = title
        story.text = text
        story.save()

        return HttpResponseRedirect(
            reverse('account:profilestory', args=(profile.uuid,story.id)))

    # if NOT POST
    else:

        context = {
            'profile': profile,
            'story': story,
            'load_trix': True
        }

        return render(request, 'account/profilestory_detail.html', context)

@user_owns_profile
def profilestory_new(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    if request.method == 'POST':

        title = request.POST['title']
        text = request.POST['text']

        story = ProfileStory(
            profile = profile,
            title = title,
            text = text
        )

        story.save()

        create_profileupdate(
            profile,
            request.user,
            'add story'
        )

        return HttpResponseRedirect(
            reverse('account:profilestory-detail', args=(profile.uuid,story.id)))

    else:

        context = {
            'profile': profile,
            'load_trix': True
        }

        return render(request, 'account/profilestory_new.html', context)

@user_owns_profile
def profilestory_edit(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.method == 'POST':

        title = request.POST['title'].strip()
        text = request.POST['text']

        story.title = title
        story.text = text
        story.save()

        return HttpResponseRedirect(
            reverse('account:profilestory-detail', args=(profile.uuid,story.id)))

    # if NOT POST
    else:

        context = {
            'profile': profile,
            'comment': story,
            'load_trix': True
        }

        return render(request, 'account/profilestory_edit.html', context)

@user_owns_profile
def profilestory_delete(request,uuid,id):

    profile = get_object_or_404(Profile,uuid=uuid)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.GET.get('confirm') and request.GET.get('confirm') == 'true':
        story.delete()

        return HttpResponseRedirect(
            reverse('account:profilestory-list', args=(profile.uuid,)))

    else:

        context = {
            'profile': profile,
            'story': story
        }

        return render(request, 'account/profilestory_delete.html', context)

@user_owns_profile
def profile_example(request,uuid):

    profile = get_object_or_404(Profile,uuid=uuid)

    context = {
        'profile': profile
    }

    return render(request, 'account/profile_example.html', context)


### NON LOGIN STUFF BELOW ### NON LOGIN STUFF BELOW

def accountrequest_new(request):

    if request.method == 'POST':

        form = AccountRequestForm(request.POST)

        if form.is_valid():

            accountrequest = form.save()

            # send a notification
            accountrequest_notification(accountrequest)

            return HttpResponseRedirect(
                reverse('account:accountrequest-confirmed', args=(accountrequest.uuid,)))

        else:
            return HttpResponse('Invalide Form. Please Try Again.')

    else:

        return render(request, 'account/accountrequest_new.html')

def accountrequest_confirmed(request,uuid):

    # get the request
    accountrequest = get_object_or_404(AccountRequest,uuid=uuid)

    context = {
        'accountrequest': accountrequest
    }

    return render(request, 'account/accountrequest_confirmed.html', context)
