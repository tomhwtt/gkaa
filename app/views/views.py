from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

import datetime
import json

from app.decorators import view_login_required, edit_login_required

from app.models import Registration, Attendee

from app.models import Profile, TeamDate, ProfileEntry, RecentProfile, EntryType, ProfileStory, ProfileImage, Event, SubEvent, DuesPayment, AccountRequest, ArmyDate, ProfileUpdate, AccountRequestNote, EventRegistration, Registration, DonationPayment, SubEventRegistration

from users.models import CustomUser

from app.forms import ProfileForm, CustomUserForm, NewProfileForm

from utils.utils import create_url_code, set_recentprofile, entry_type_title, update_teamdate_string, clean_trix_text, create_short_code

from utils.postmark import send_user_account_notice, send_event_email
from utils.boto import put_aws_object,delete_aws_object

@view_login_required
def app_index(request):

    if request.method == 'POST':

        query = request.POST['query'].strip()
        return HttpResponseRedirect(reverse('app:search') + '?q=' + query)

    else:

        # get RecentProfile(s)
        recent_list = RecentProfile.objects.all()[:5]

        context = {
            'recent_list': recent_list
        }

        return render(request, 'app/index.html', context)

@view_login_required
def app_search(request):

    #if request.GET.get('q'):

    query = request.GET.get('q')

    profile_set = Profile.objects.filter(
        Q(first_name__icontains = query)|
        Q(last_name__icontains = query)|
        Q(nickname__icontains = query)|
        Q(aka__icontains = query)|
        Q(search_field__icontains = query)
    )

    #else:
        #profile_set = None
        #query = 'Not Here'

    context = {
        'query': query,
        'profile_set': profile_set
    }

    return render(request, 'app/search.html', context)

@view_login_required
def profile_detail(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    # create a RecentProfile
    set_recentprofile(profile)

    context = {
        'profile': profile,
        'entry_list': profile.entry_list(),
        'image_set': profile.image_list(),
        'story_set': profile.profilestory_set.all()
    }

    return render(request, 'app/profile_detail.html', context)

@edit_login_required
def profile_edit_view(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    if request.method == 'POST':

        form = ProfileForm(request.POST,instance=profile)

        if form.is_valid():

            profile = form.save()



            return HttpResponseRedirect(
                reverse('app:profile-edit', args=(profile.id,)) + str('?s=updated'))

        else:
            return HttpResponse('Form is not valid')

    else:

        set_recentprofile(profile)

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'update_notice': update_notice
        }


        return render(request, 'app/profile_edit.html', context)

@edit_login_required
def profile_dates(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    if request.method == 'POST':

        team_start_year = request.POST['team_start_year'].strip()
        team_end_year = request.POST['team_end_year'].strip()
        army_start_year = request.POST['army_start_year'].strip()
        army_end_year = request.POST['army_end_year'].strip()

        deceased_year = request.POST['deceased_year'].strip()
        deceased_date = request.POST['deceased_date'].strip()

        # add TeamDates
        if team_start_year:

            if not team_end_year:
                team_end_year = None

            teamdate = TeamDate(
                start_year = team_start_year,
                end_year = team_end_year,
                profile = profile
            )

            teamdate.save()

            update_teamdate_string(profile)

        # add ArmyDates
        if army_start_year or army_end_year:

            if not army_end_year:
                army_end_year = None

            armydate = ArmyDate(
                start_year = army_start_year,
                end_year = army_end_year,
                profile = profile
            )

            armydate.save()

        # update deceased dates
        if deceased_date:
            profile.deceased_date = deceased_date
        else:
            profile.deceased_date = None

        if deceased_year:
            profile.deceased_year = deceased_year
        else:
            deceased_year = None

        profile.save()

        return HttpResponseRedirect(
            reverse('app:profile-dates', args=(profile.id,))+ str('?s=updated'))

    # if NOT POST
    else:

        teamdate_set = profile.teamdate_set.all()
        armydate_set = profile.armydate_set.all()

        if profile.deceased_date:
            deceased_date = profile.deceased_date.strftime('%Y-%m-%d')
        else:
            deceased_date = ''

        if profile.deceased_year:
            deceased_year = profile.deceased_year
        else:
            deceased_year = ''

        # show a notification after update
        if request.GET.get('s') and request.GET.get('s') == 'updated':
            update_notice = True
        else:
            update_notice = False

        context = {
            'profile': profile,
            'teamdate_set': teamdate_set,
            'armydate_set': armydate_set,
            'deceased_date': deceased_date,
            'deceased_year': deceased_year,
            'update_notice': update_notice
        }

        return render(request, 'app/profile_dates.html', context)

@edit_login_required
def teamdate_delete(request,pk):

    # get the TeamDate
    teamdate = get_object_or_404(TeamDate,pk=pk)

    # set the Profile befor you delete the date
    profile = teamdate.profile

    # delete the date
    teamdate.delete()

    update_teamdate_string(profile)

    return HttpResponseRedirect(
        reverse('app:profile-dates', args=(profile.id,)))

@edit_login_required
def armydate_delete(request,pk):

    # get the TeamDate
    armydate = get_object_or_404(ArmyDate,pk=pk)

    # set the Profile befor you delete the date
    profile = armydate.profile

    # delete the date
    armydate.delete()

    return HttpResponseRedirect(
        reverse('app:profile-dates', args=(profile.id,)))

@view_login_required
def entry_detail(request,pk):

    entry = get_object_or_404(ProfileEntry,pk=pk)
    profile = entry.profile

    context = {
        'profile': profile,
        'entry': entry
    }

    return render(request, 'app/entry.html', context)

@view_login_required
def profile_entries(request,pk,type):

    profile = get_object_or_404(Profile,pk=pk)
    entrytype = get_object_or_404(EntryType,pk=type)

    if request.method == 'POST':

        # see if show_on_home is checked
        try:
            home_highlight = request.POST['home']
            show_on_home = True
        except:
            show_on_home = False

        entry = ProfileEntry(
            profile = profile,
            entrytype = entrytype,
            text = request.POST['text'].strip(),
            show_on_home = show_on_home
        )

        entry.save()

        return HttpResponseRedirect(
            reverse('app:profile-entries', args=(profile.id,type)))

    # if NOT POST
    else:

        entry_list = ProfileEntry.objects.filter(
            profile = profile,
            entrytype = entrytype
        )


        type_list = EntryType.objects.filter(
            sort_order__gt=0
        ).order_by(
            'sort_order'
        )

        context = {
            'profile': profile,
            'entry_list': entry_list,
            'title': entrytype.title,
            'singular': entrytype.singular,
            'type_list': type_list
        }

        return render(request, 'app/entry_list.html', context)

@edit_login_required
def profile_new(request):

    if request.method == 'POST':

        form = NewProfileForm(request.POST)

        if form.is_valid():

            profile = form.save(commit=False)
            profile.url_code = create_url_code()
            profile.save()


            start_year = request.POST['start_year'].strip()
            end_year = request.POST['end_year'].strip()

            if start_year and end_year:

                # add the TeamDates
                teamdate = TeamDate(
                    profile = profile,
                    start_year = start_year,
                    end_year = end_year
                )

                teamdate.save()

            elif start_year and not end_year:

                # add the TeamDates
                teamdate = TeamDate(
                    profile = profile,
                    start_year = request.POST['start_year'].strip()
                )

                teamdate.save()

            update_teamdate_string(profile)


            return HttpResponseRedirect(
                reverse('app:profile-detail', args=(profile.id,)))

        else:
            return HttpResponse('Invalid Form')

    # if NOT POST
    else:

        context = {

        }

        return render(request, 'app/profile_new.html', context)

@edit_login_required
def entry_delete(request,pk):

    # get the ProfileEntry
    entry = get_object_or_404(ProfileEntry,pk=pk)

    # set the Profile and EntryType before you delete it
    id = entry.profile.id
    type = entry.entrytype.id

    # delete the entry
    entry.delete()

    return HttpResponseRedirect(
        reverse('app:profile-entries', args=(id,type)))

@edit_login_required
def profile_split_entry_view(request,pk):

    # get the profile
    profile = get_object_or_404(Profile,pk=pk)

    # OldHighlights
    old_list = profile.oldhighlight_set.all()

    context = {
        'profile': profile,
        'old_list': old_list
    }

    return render(request, 'app/split_entry.html', context)

@edit_login_required
def profile_priority_list(request):

    profile_list = Profile.objects.filter(
        type = 1,
        update_complete = False
    ).order_by('-update_priority')[:20]

    context = {
        'profile_list': profile_list
    }

    return render(request, 'app/profile_priority_list.html', context)

@edit_login_required
def profileupdate_list(request):

    update_list = ProfileUpdate.objects.all().select_related(
        'profile'
    )[:36]

    context = {
        'update_list': update_list
    }

    return render(request, 'app/profileupdate_list.html', context)

@edit_login_required
def event_list(request):

    event_set = Event.objects.all().order_by(
        '-date'
    )

    context = {
        'event_set': event_set
    }

    return render(request, 'app/event_list.html', context)

@edit_login_required
def duespayment_list(request):

    if request.method == 'POST':

        q = request.POST['q'].strip()

        payment_list = DuesPayment.objects.filter(
            Q(name__icontains = q)|
            Q(email__icontains = q)
        )

        title = ''

    else:
        payment_list = DuesPayment.objects.all()[:10]
        title = 'Showing Last 10 Payments'


    context = {
        'payment_list': payment_list,
        'title': title
    }

    return render(request, 'app/duespayment_list.html', context)

@edit_login_required
def event_detail(request,pk):

    event = get_object_or_404(Event,pk=pk)

    context = {
        'event': event,
        'subevent_set': event.subevent_set.all()
    }

    return render(request, 'app/event_detail.html', context)

@edit_login_required
def event_email(request,pk):

    event = get_object_or_404(Event,pk=pk)

    if request.method == 'POST':

        subject = request.POST['subject'].strip()
        text = request.POST['text']
        html = clean_trix_text(text)


        # set the attendee list
        reg_list = event.eventregistration_set.all()

        # so we only send to the same email once
        # keep a list of ones you sent
        email_list = []

        # create a message array
        message_array = []

        for reg in reg_list:

            if reg.email not in email_list:

                message_obj = {
                    "From": "GKAA Support <notifications@goldenknightsalumni.org>",
                    "To" : reg.email,
                    "ReplyTo": "goldenknightsalumni@gmail.com",
                    "MessageStream": "broadcast",
                    "TemplateAlias": "event-email",
                    "TrackOpens": "true",
                    "TemplateModel":{
                        "name": reg.name,
                        "subject": subject,
                        "html": str(html)
                    }
                }

                message_array.append(message_obj)

                # then add the email to the email list so
                # we only send them one email
                email_list.append(reg.email)

        # send the batch template
        send = send_event_email(
            message_array
        )

        qs = '?s=sent&a=' + str(len(message_array))

        return HttpResponseRedirect(
            reverse('app:event-email', args=(event.id,)) + qs )

    else:

        if request.GET.get('s'):
            notify = True
        else:
            notify = False

        if request.GET.get('a'):
            num_sent = request.GET.get('a')
        else:
            num_sent = ''


        context = {
            'event': event,
            'load_trix': True,
            'notify': notify,
            'num_sent': num_sent
        }

        return render(request, 'app/event_email.html', context)

@edit_login_required
def subevent_detail(request,pk):

    subevent = get_object_or_404(SubEvent,pk=pk)

    reg_set = subevent.subeventregistration_set.filter(
        quantity__gt = 0,
        eventregistration__cancelled = 0
    ).exclude(
        eventregistration__stripe_charge_id = ''
    )

    reg_list = []
    num_attendees = 0

    for reg in reg_set:

        # set the EventRegistration so I can update it
        event_reg = reg.eventregistration
        save_event_reg = False

        name = reg.eventregistration.name

        name_split = name.split(' ')

        last_name = name_split[len(name_split)-1]

        first_name = name[:(len(name)-len(last_name))-1].strip()

        reg_obj = {
            'last_name': last_name,
            'first_name': first_name,
            'quantity': reg.quantity
        }

        reg_list.append(reg_obj)

        # increment the attendee list if they are not comped
        if not event_reg.comped:
            num_attendees += reg.quantity

        # update the first name and last name
        # next year, we are going to ask for them instead
        if not event_reg.first_name:
            event_reg.first_name = first_name
            save_event_reg = True

        if not event_reg.last_name:
            event_reg.last_name = last_name
            save_event_reg = True

        if save_event_reg:
            event_reg.save()

    reg_list = sorted(
        reg_list,
        key = lambda reg: reg['last_name']
    )

    context = {
        'event': subevent.event,
        'subevent': subevent,
        'reg_list': reg_list,
        'num_attendees': num_attendees
    }

    return render(request, 'app/subevent_detail.html', context)

@edit_login_required
def eventregistration_new(request,pk):

    event = get_object_or_404(Event,pk=pk)

    if request.method == 'POST':

        name = request.POST['name'].strip()
        type = request.POST['type']
        stripe_charge_id = 'comped_manual_add'
        subevent_string = request.POST['subevent_string']

        if request.POST['email']:
            email = request.POST['email'].strip()
        else:
            email = 'goldenknightsalumni@gmail.com'

        event_reg = EventRegistration(
            event = event,
            name = name,
            email = email,
            short_code = create_short_code(),
            type = type,
            stripe_charge_id = stripe_charge_id
        )

        event_reg.save()

        # set the subevent array
        subevent_array = json.loads(subevent_string)

        for sub in subevent_array:

            subevent = SubEvent.objects.get(pk=sub['id'])

            subevent_reg = SubEventRegistration(
                eventregistration = event_reg,
                subevent = subevent,
                quantity = sub['qty']
            )

            subevent_reg.save()

        return HttpResponseRedirect(
            reverse('app:eventregistration-detail', args=(event_reg.id,)) + str('?s=added'))

    else:

        context = {
            'event': event,
            'subevent_set': event.subevent_set.all()

        }

        return render(request, 'app/eventregistration_new.html', context)

@edit_login_required
def eventregistration_detail(request,pk):

    reg = get_object_or_404(EventRegistration,pk=pk)

    subevent_reg = reg.subeventregistration_set.all()

    context = {
        'reg': reg,
        'subevent_reg': subevent_reg,
        'event': reg.event

    }

    return render(request, 'app/eventregistration_detail.html', context)

@edit_login_required
def accountrequest_list(request):

    request_set = AccountRequest.objects.filter(
        complete__isnull = True
    )

    if request.GET.get('s') and request.GET.get('s') == 'pending':
        request_set = request_set.filter(
            pending_verification = True
        )

    elif request.GET.get('s') and request.GET.get('s') == 'later':
        request_set = request_set.filter(
            later = True
        )

    else:
        request_set = request_set.filter(
            pending_verification = False,
            later = False
        )

    request_list = []



    context = {
        'request_set': request_set,
        'num': request_set.count()
    }

    return render(request, 'app/accountrequest_list.html', context)

@edit_login_required
def accountrequest_detail(request,pk):

    accountrequest = get_object_or_404(AccountRequest,pk=pk)

    if request.method == 'POST':

        note_text = request.POST['text'].strip()

        # split up the note text to create a reminder date
        note_text_split = note_text.split(' ')
        last_word = note_text_split[len(note_text_split)-1]

        # update the pending date?
        if last_word.isnumeric():
            days = int(last_word)
            pending_date = datetime.datetime.now() + datetime.timedelta(days=days)
        else:
            pending_date = None

        if pending_date:

            accountrequest.pending_date = pending_date
            accountrequest.save()

            note_text = note_text[:len(note_text)-len(last_word)]


        note = AccountRequestNote(
            accountrequest = accountrequest,
            note = note_text,
            user = request.user
        )

        note.save()

        return HttpResponseRedirect(
            reverse('app:accountrequest-detail', args=(accountrequest.id,)))

    # if not POST
    else:

        if accountrequest.pending_verification:
            status = 'pending'
        elif accountrequest.later:
            status = 'later'
        else:
            status = 'new'


        note_set = accountrequest.accountrequestnote_set.all()

        # create a list of possible Profile(s)
        name_split = accountrequest.name.split(' ')

        # the last name in the list
        # somtimes there are 3, like (Charles Keller Brown)
        last_name = name_split[len(name_split)-1]

        matching_profiles = Profile.objects.filter(
            last_name__icontains = last_name
        ).exclude(
            user__isnull = False
        )

        # check their email for other activity
        email = accountrequest.email_address
        email_activity_list = []

        email_dues = DuesPayment.objects.filter(
            email = email
        )

        for email in email_dues:

            email_obj = {
                'type': 'Dues Payment',
                'date': email.date
            }

            email_activity_list.append(email_obj)

        email_donation = DonationPayment.objects.filter(
            email = email
        )

        for email in email_donation:

            email_obj = {
                'type': 'Donation',
                'date': email.date
            }

            email_activity_list.append(email_obj)

        email_registration = Registration.objects.filter(
            email_address = email
        )

        for email in email_registration:

            email_obj = {
                'type': 'Old Registrations',
                'date': email.date
            }

            email_activity_list.append(email_obj)

        email_event = EventRegistration.objects.filter(
            email = email
        )

        for email in email_event:

            email_obj = {
                'type': 'Event Registration',
                'date': email.date
            }

            email_activity_list.append(email_obj)

        # do they have an account?
        try:
            customuser = CustomUser.objects.get(
                email=accountrequest.email_address
            )
        except:
            customuser = None

        try:
            profile = Profile.objects.get(
                user = customuser
            )
        except:
            profile = None


        context = {
            'r': accountrequest,
            'note_set': note_set,
            'status': status,
            'profile_list': matching_profiles,
            'email_activity_list': email_activity_list,
            'customuser': customuser,
            'profile': profile
        }

        return render(request, 'app/accountrequest_detail.html', context)

@edit_login_required
def accountrequest_delete(request,pk):

    accountrequest = get_object_or_404(AccountRequest,pk=pk)
    accountrequest.delete()

    return HttpResponseRedirect(reverse('app:accountrequest-list'))

@edit_login_required
def accountrequest_set_pending(request,pk):

    ar = get_object_or_404(AccountRequest,pk=pk)

    ar.pending_verification = True
    ar.pending_date = datetime.datetime.now() + datetime.timedelta(days=2)
    ar.save()

    return HttpResponseRedirect(
        reverse('app:accountrequest-detail', args=(ar.id,)))

@edit_login_required
def accountrequest_set_later(request,pk):

    ar = get_object_or_404(AccountRequest,pk=pk)

    ar.later = True
    ar.save()

    return HttpResponseRedirect(
        reverse('app:accountrequest-detail', args=(ar.id,)))

@edit_login_required
def accountrequest_complete(request,pk):

    ar = get_object_or_404(AccountRequest,pk=pk)

    ar.complete = datetime.datetime.now()
    ar.save()

    return HttpResponseRedirect(
        reverse('app:accountrequest-detail', args=(ar.id,)))

@edit_login_required
def customuser_new(request,pk):

    # get the AccountRequest
    r = get_object_or_404(AccountRequest,pk=pk)

    if request.method == 'POST':

        form = CustomUserForm(request.POST)

        if form.is_valid():
            user = form.save()

            # reset the AccountRequest info
            r.complete = datetime.datetime.now()
            r.pending_verification = False
            r.later = False
            r.pending_date = None
            r.save()

            return HttpResponseRedirect(
                reverse('app:customuser-detail', args=(user.id,)))

        else:
            return HttpResponse('Invalid Form')

    else:

        context = {
            'r': r,
            'has_account': r.has_account()
        }


        return render(request, 'app/user_new.html', context)

@edit_login_required
def customuser_detail(request,pk):

    # get the AccountRequest
    user = get_object_or_404(CustomUser,pk=pk)

    # try to find a profile with this user first
    try:
        profile = Profile.objects.get(user=user)
        matching_profiles = None

    except:
        profile = None

        name_split = user.name.split(' ')

        # the last name in the list
        # somtimes there are 3, like (Charles Keller Brown)
        last_name = name_split[len(name_split)-1]

        matching_profiles = Profile.objects.filter(
            last_name__icontains = last_name
        ).exclude(
            user__isnull = False
        )

    if request.GET.get('n'):
        notify = True
    else:
        notify = False


    context = {
        'user': user,
        'profile': profile,
        'matching_profiles': matching_profiles,
        'notify': notify
    }


    return render(request, 'app/user_detail.html', context)

@edit_login_required
def customuser_list(request):

    if request.method == 'POST':

        user_set = CustomUser.objects.filter(
            name__icontains = request.POST['q']
        )[:10]

    else:

        user_set = CustomUser.objects.all()[:10]

    context = {
        'user_set': user_set
    }


    return render(request, 'app/user_list.html', context)

@edit_login_required
def profile_set_user(request,pk,id):


    profile = get_object_or_404(Profile,pk=pk)
    user = get_object_or_404(CustomUser,pk=id)

    profile.user = user
    profile.save()

    return HttpResponseRedirect(
        reverse('app:customuser-detail', args=(user.id,)))

@edit_login_required
def send_user_account_email(request,pk):

    user = get_object_or_404(CustomUser,pk=pk)

    # create a first name
    first_name = user.name.split(' ')[0]

    send_user_account_notice(
        name = first_name,
        email = user.email
    )

    return HttpResponseRedirect(
        reverse('app:customuser-detail', args=(user.id,)) + str('?n=email'))

@edit_login_required
def profilestory_list(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    story_set = profile.profilestory_set.all()

    context = {
        'profile': profile,
        'story_set': story_set
    }

    return render(request, 'app/profilestory_list.html', context)

@edit_login_required
def profilestory_new(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    if request.method == 'POST':

        title = request.POST['title']
        text = request.POST['text']

        story = ProfileStory(
            profile = profile,
            title = title,
            text = text
        )

        story.save()

        return HttpResponseRedirect(
            reverse('app:profilestory-detail', args=(profile.id,story.id)))

    else:

        context = {
            'profile': profile,
            'load_trix': True
        }

        return render(request, 'app/profilestory_new.html', context)

@edit_login_required
def profilestory_detail(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.method == 'POST':

        title = request.POST['title'].strip()
        text = request.POST['text']

        story.title = title
        story.text = text
        story.save()

        return HttpResponseRedirect(
            reverse('app:profilestory-detail', args=(profile.uuid,story.id)))

    # if NOT POST
    else:

        context = {
            'profile': profile,
            'story': story,
            'load_trix': True
        }

        return render(request, 'app/profilestory_detail.html', context)

@edit_login_required
def profilestory_edit(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.method == 'POST':

        title = request.POST['title'].strip()
        text = request.POST['text']

        story.title = title
        story.text = text
        story.save()

        return HttpResponseRedirect(
            reverse('app:profilestory-detail', args=(profile.id,story.id)))

    # if NOT POST
    else:

        context = {
            'profile': profile,
            'story': story,
            'load_trix': True
        }

        return render(request, 'app/profilestory_edit.html', context)

@edit_login_required
def profilestory_delete(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
    story = get_object_or_404(ProfileStory,pk=id)

    if request.GET.get('confirm') and request.GET.get('confirm') == 'true':
        story.delete()

        return HttpResponseRedirect(
            reverse('app:profilestory-list', args=(profile.id,)))

    else:

        context = {
            'profile': profile,
            'story': story
        }

        return render(request, 'app/profilestory_delete.html', context)

@edit_login_required
def profileimage_list(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

    image_set = profile.profileimage_set.all()

    context = {
        'profile': profile,
        'image_set': image_set
    }

    return render(request, 'app/profileimage_list.html', context)

@edit_login_required
def profileimage_detail(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
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

    context = {
        'profile': profile,
        'image': image,
        'profile_image': profile_image,
        'roster_image': roster_image,
        'notify': notify
    }

    return render(request, 'app/profileimage_detail.html', context)

@edit_login_required
def profileimage_new(request,pk):

    profile = get_object_or_404(Profile,pk=pk)

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

                try:
                    set_profile = request.POST['set_profile']
                    profile_image = True
                except:
                    profile_image = False

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
                    reverse('app:profileimage-list',
                        args=(profile.id,)))

        except:
            return HttpResponse('No File Chosen')

    else:

        context = {
            'profile': profile
        }

        return render(request, 'app/profileimage_new.html', context)

@edit_login_required
def profileimage_edit(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
    image = get_object_or_404(ProfileImage,pk=id)


    if request.method == 'POST':

        image.caption = request.POST['caption'].strip()
        image.year = request.POST['year'].strip()
        image.credit = request.POST['credit'].strip()

        image.save()

        return HttpResponseRedirect(
            reverse('app:profileimage-edit',
                args=(profile.id,image.id))+ str('?s=updated'))

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

        return render(request, 'app/profileimage_edit.html', context)

@edit_login_required
def profileimage_delete(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
    image = get_object_or_404(ProfileImage,pk=id)

    if request.GET.get('confirm') and request.GET.get('confirm') == 'true':

        delete_aws_object(
            bucket = 'gkaa-imgix',
            key = 'images/profiles/' + image.name
        )

        # delete the ProfileImage
        image.delete()

        return HttpResponseRedirect(
            reverse('app:profileimage-list', args=(profile.id,)))

    # if delete not confirmed
    else:

        context = {
            'profile': profile,
            'image': image
        }

        return render(request, 'app/profileimage_delete.html', context)

@edit_login_required
def profileimage_profile_image(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
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
        reverse('app:profileimage-detail',
            args=(profile.id,image.id)) + str('?s=updated'))

@edit_login_required
def profileimage_roster_image(request,pk,id):

    profile = get_object_or_404(Profile,pk=pk)
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
        reverse('app:profileimage-detail',
            args=(profile.id,image.id)) + str('?s=updated'))
