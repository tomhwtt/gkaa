from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.conf import settings

from django.http import JsonResponse

import json
import datetime
import stripe

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from app.models import Event, SubEvent, SubEventPricing, EventRegistration, SubEventRegistration, DuesPayment

from utils.postmark import send_contactrequest_email
from utils.utils import create_safe_email, create_short_code, check_dues_by_email
from utils.stripe import create_stripe_charge

def event_detail(request,event_code):

    # get the event
    event = get_object_or_404(Event, short_code=event_code)

    context = {
        'event': event,
        'subevent_set': event.subevent_set.all()

    }

    return render(request, 'website/event_detail.html', context)

def event_register(request,event_code):

    # get the event
    event = get_object_or_404(Event, short_code=event_code)

    # subeventlist
    subevent_list = event.subevent_set.all()

    # if there is an email validation error
    if request.GET.get('e') and request.GET.get('e') == 'email':
        email_error = True
    else:
        email_error = False

    context = {
        'event': event,
        'subevent_list': subevent_list,
        'email_error': email_error

    }

    return render(request, 'website/event_register.html', context)

def event_registration_detail(request,short_code):

    # get the EventRegistration
    registration = get_object_or_404(EventRegistration,short_code=short_code)

    subevent_list = []

    for sub in registration.cart()['items']:

        if sub['quantity']:
            subevent_list.append(sub)


    context = {
        'registration': registration,
        'subevent_list': subevent_list,
        'total': registration.amount,
        'add_dues': registration.cart()['add_dues']

    }

    return render(request, 'website/event_registration_detail.html', context)

def event_registration_payment(request,short_code):

    # get the EventRegistration
    registration = get_object_or_404(EventRegistration,short_code=short_code)
    cart_total = registration.cart()['total']

    # if there is no balance due update stripe_charge_id
    if not cart_total:
        registration.stripe_charge_id = 'no-balance-due'
        registration.save()

    # they can only be on this page if they have not paid yet
    if not registration.stripe_charge_id:

        # is the Event in test_mode?
        test_mode = registration.event.test_mode

        subevent_set = registration.subeventregistration_set.all()

        # have dues been paid this year?
        dues_paid = check_dues_by_email(registration.email)

        # set the stripe key
        if test_mode:
            stripe_pk = settings.STRIPE_PUBLISHABLE_KEY_TEST
        else:
            stripe_pk = settings.STRIPE_PUBLISHABLE_KEY

        if request.GET.get('e'):
            error_code = request.GET.get('e')
        else:
            error_code = None

        # we only need the stripe stuff if there is a cart_total
        if cart_total:
            show_new_stripe = True
        else:
            show_new_stripe = False

        context = {
            'registration': registration,
            'dues_paid': dues_paid,
            'cart_items': registration.cart()['items'],
            'cart_total': cart_total,
            'stripe_pk': stripe_pk,
            'show_new_stripe': show_new_stripe,
            'error_code': error_code,
            'test_mode': registration.event.test_mode,
            'add_dues': registration.cart()['add_dues']

        }

        return render(request, 'website/event_payment_detail.html', context)

    # if they have already paid
    else:

        # redirect to detail page
        return HttpResponseRedirect(
            reverse('website:eventregistration-detail',
                args=(registration.short_code,)))

def event_registration_complete(request,short_code):

    # get the EventRegistration
    registration = get_object_or_404(EventRegistration,short_code=short_code)
    total = registration.cart()['total']

    # if no balance due, we can complete the registration
    if not total:

        registration.stripe_charge_id = 'no_balance_due'
        registration.save()

        # redirect to success page
        return HttpResponseRedirect(
            reverse('website:eventregistration-detail',
            args=(registration.short_code,)))

    # if there is a balance due, they have to pay first
    else:

        return HttpResponseRedirect(
            reverse('website:eventregistration-payment',
            args=(registration.short_code,)))

def event_registration_charge(request,short_code):

    # get the EventRegistration
    registration = get_object_or_404(EventRegistration,short_code=short_code)

    # set the form fields
    token = request.POST['stripe_token']

    # set the total
    total = registration.cart()['total']

    # create the stripe charge
    charge = create_stripe_charge(
        token = token,
        amount = total,
        description = registration.event.name,
        receipt_email = registration.email,
        test_charge = registration.event.test_mode
    )

    # try to save the charge
    # if charge failed, this will fail and redirect them back to payment page
    try:

        registration.amount = total
        registration.stripe_charge_id = charge.id
        registration.save()

        # if we need to add dues
        if registration.cart()['add_dues']:

            duespayment = DuesPayment(
                name = registration.name,
                email = registration.email,
                amount = 50,
                stripe_charge_id = charge.id,
                year = datetime.datetime.today().year
            )

            duespayment.save()

            # then update the EventRegistration with a tag
            registration.dues_added = True
            registration.save()

        # redirect to success page
        return HttpResponseRedirect(
            reverse('website:eventregistration-detail',
            args=(registration.short_code,)))

    except:

        # redirect back to payment page
        return HttpResponseRedirect(
            reverse('website:eventregistration-payment',
            args=(registration.short_code,)) + '?e=' + charge)

# AJAX Events
@require_POST
def event_register_new(request):

    if request.is_ajax():

        # set type and email
        type = request.POST['type']
        name = request.POST['name'].strip()
        email = request.POST['email'].strip()
        event_code = request.POST['event'].strip()

        # get the event
        event = Event.objects.get(
            short_code = event_code
        )

        # set the subevent string
        subevent_string = request.POST['subevent_string']
        subevent_array = json.loads(subevent_string)

        # create a new EventRegistration
        registration = EventRegistration(
            email = email,
            name = name,
            short_code = create_short_code(),
            type = type,
            event = event
        )

        registration.save()

        # create SubEventRegistration(s)
        for sub in subevent_array:

            # get the SubEvent
            subevent = SubEvent.objects.get(
                pk = sub['id']
            )

            subregistration = SubEventRegistration(
                eventregistration = registration,
                subevent = subevent,
                quantity = sub['qty']
            )

            subregistration.save()

        return JsonResponse({'success': str(registration.short_code) })

    # if NOT Ajax
    else:
        return HttpResponse('is HTTP')


# a list of SubEvents for an Event
def checkin_event_detail(request,slug):

    # get the reunion
    event = Event.objects.get(
        short_code = 'reunion-2021'
    )

    context = {
        'event': event,
        'subevent_set':  event.subevent_set.all()
    }

    return render(request, 'website/checkin/event_detail.html', context)

#  SubEvent detail
def checkin_subevent_detail(request,slug,pk):

    # get the Event
    event = Event.objects.get(
        short_code = slug
    )

    # get the SubEvent
    subevent = SubEvent.objects.get(
        event = event,
        pk = pk
    )

    # Get the SubEventRegistration list
    reg_set = subevent.subeventregistration_set.filter(
        quantity__gt=0
    )


    # do we want to show checked in (c)?
    if request.GET.get('c'):
        show_checked_in = True

    # or do we want to show not checked in?
    else:
        show_checked_in = False

    reg_list = []
    total_reg = 0
    total_checked_in = 0
    total_not_checked_in = 0

    for reg in reg_set:

        # increment the above numbers
        if reg.checked_in_date:
            total_checked_in += reg.quantity
        else:
            total_not_checked_in += reg.quantity

        name = reg.eventregistration.name

        name_split = name.split(' ')

        last_name = name_split[len(name_split)-1]

        first_name = name[:(len(name)-len(last_name))-1].strip()

        full_name = last_name + ', ' + first_name

        if len(full_name) > 22:
            full_name = full_name[:22] + '..'

        reg_obj = {
            'id': reg.id,
            'full_name': full_name,
            'quantity': reg.quantity,
            'checked_in': reg.checked_in_date
        }

        if reg.checked_in_date and show_checked_in:
            reg_list.append(reg_obj)
        elif not reg.checked_in_date and not show_checked_in:
            reg_list.append(reg_obj)

    reg_list = sorted(
        reg_list,
        key = lambda reg: reg['full_name']
    )

    context = {
        'reg_list': reg_list,
        'total_checked_in': total_checked_in,
        'total_not_checked_in': total_not_checked_in,
        'num_reg': total_checked_in + total_not_checked_in,
        'event': event,
        'subevent': subevent
    }

    return render(request, 'website/checkin/subevent_detail.html', context)

def checkin_subeventregistration(request,pk):

    # get the SubEventRegistration
    reg = get_object_or_404(SubEventRegistration,pk=pk)

    # set the event and subevent for redirect
    slug = reg.subevent.event.short_code
    id = reg.subevent.id

    # set checked in
    reg.checked_in = True
    reg.save()

    context = {
        'name': reg.eventregistration.name,
        'quantity': reg.quantity,
        'slug': slug,
        'id': id
    }

    return render(request, 'website/checkin/subeventregistration_detail.html', context)

def checkin_subeventregistration_detail(request,pk):

    # get the SubEventRegistration
    reg = get_object_or_404(SubEventRegistration,pk=pk)

    context = {
        'reg': reg,
        'event': reg.subevent.event,
        'subevent': reg.subevent,
        'name': reg.eventregistration.name,
        'quantity': reg.quantity,
    }

    return render(request, 'website/checkin/subeventregistration_detail.html', context)

def checkin_subeventregistration_checkin(request,pk):

    # get the SubEventRegistration
    reg = get_object_or_404(SubEventRegistration,pk=pk)

    # set checked in
    if reg.checked_in_date:
        reg.checked_in_date = None
    else:
        reg.checked_in_date = datetime.datetime.now()

    reg.save()

    return HttpResponseRedirect(
        reverse('website:checkin-subeventregistration-detail', args=(reg.id,)))
