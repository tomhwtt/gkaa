import stripe
import json
import datetime

from django.conf import settings

from app.models import EventRegistration, Profile, DuesPayment, DonationPayment

def get_stripe_key(test_charge):

    # set the stripe key
    if test_charge:
        return settings.STRIPE_SECRET_KEY_TEST
    else:
        return settings.STRIPE_SECRET_KEY

def create_stripe_charge(token,amount,description,receipt_email,test_charge):

    stripe.api_key = get_stripe_key(test_charge)

    # try to charge the card
    try:

        # the amount is in dollars, convert to Stripe format
        stripe_amount = int((amount * 100))

        charge = stripe.Charge.create(
            amount = stripe_amount,
            currency ="usd",
            source = token,
            description = description,
            receipt_email = receipt_email
            )

        return charge

    # if there was an error charging the card
    except stripe.error.CardError as e:

        err = e.json_body['error']

        error_text = err.get('code')

        return error_text

def stripe_charge_registration(payment_type_id,token):

    # get the registration
    registration = EventRegistration.objects.get(
        short_code = payment_type_id
    )

    # if they opted to pay their dues at this time
    if registration.add_dues:

        amount = ((registration.each * registration.quantity) + 50)
        description = registration.event.name + ' & Dues'

    else:

        amount = registration.each * registration.quantity
        description = registration.event.name

    if registration.event.test_mode:
        test_charge = True
    else:
        test_charge = False

    charge = create_stripe_charge(
        test_charge = test_charge,
        token = token,
        amount = amount,
        description = description,
        receipt_email = registration.email
    )

    # process the payment
    try:

        return_obj = {
            'status': 'success',
            'status_text': charge.id,
            'return_url': '/event/registration/' + str(registration.short_code) + '/'
        }

        registration.total = amount
        registration.charge_id = charge.id
        registration.save()

    # if there was an error, return it and give them instructions
    except:

        return_obj = {
            'status': 'error',
            'status_text': charge,
            'return_url': '/event/registration/' + str(registration.short_code) + '/payment/?e=' + str(charge)
        }


    return return_obj

def stripe_charge_dues(type_id,token,amount,email):

    # get the Profile
    profile = Profile.objects.get(uuid=type_id)

    # create a name
    full_name = profile.first_name + ' ' + profile.last_name

    # current year
    current_year = int(datetime.datetime.now().year)

    # if they have already paid their dues, this is a donation
    if profile.dues_paid():
        dues_amount = 0
        donation_amount = amount
    else:
        dues_amount = 50
        donation_amount = amount - 50

    if donation_amount > 0:
        donation_amount = donation_amount
    else:
        donation_amount = 0

    # if you paid dues and donation
    if dues_amount and donation_amount:
        description = str(current_year) + ' GKAA Dues & Donation'
        charge_amount = dues_amount + donation_amount

    # if you just paid dues
    elif dues_amount and not donation_amount:
        description = str(current_year) + ' GKAA Dues'
        charge_amount = dues_amount

    else:
        description = 'GKAA Donation (' + str(current_year) + ')'
        charge_amount = donation_amount + dues_amount

    if settings.DEBUG:
        test_charge = True
    else:
        test_charge = False

    charge = create_stripe_charge(
        test_charge = test_charge,
        token = token,
        amount = charge_amount,
        description = description,
        receipt_email = email.lower()
    )

    # Create a Dues Payment
    # if there is no charge.id, it will use the except code instead
    try:

        # create a Dues Payment
        duespayment = DuesPayment(
            name = full_name.strip(),
            email = email.lower(),
            date = datetime.datetime.now(),
            amount = dues_amount,
            donation = donation_amount,
            stripe_charge_id = charge.id,
            year = current_year,
            profile = profile
        )

        duespayment.save()

        return_obj = {
            'status': 'success',
            'status_text': charge.id,
            'return_url': '/dues/' + str(duespayment.uuid) + '/success/'
        }

    except:

        return_obj = {
            'status': 'error',
            'status_text': charge,
            'return_url': '/pay-dues/' + str(profile.uuid) + '/?e=' + str(charge)
        }


    return return_obj

def stripe_charge_donation(token,amount,name,email,note):

    if settings.DEBUG:
        test_charge = True
    else:
        test_charge = False

    # current year
    current_year = int(datetime.datetime.now().year)

    description = 'GKAA Donation (' + str(current_year) + ')'

    # charge the card
    charge = create_stripe_charge(
        test_charge = test_charge,
        token = token,
        amount = amount,
        description = description,
        receipt_email = email.lower()
    )

    # create a DonationPayment
    try:

        donation = DonationPayment(
            name = name,
            email = email.lower(),
            amount = amount,
            note = note,
            stripe_charge_id = charge.id
        )

        donation.save()

        return_obj = {
            'status': 'success',
            'status_text': charge.id,
            'return_url': '/donation/' + str(donation.uuid) + '/success/'
        }

    except:

        return_obj = {
            'status': 'error',
            'status_text': charge,
            'return_url': '/donate/?e=' + str(charge)
        }

    return return_obj
