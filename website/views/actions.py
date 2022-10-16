from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from random import randrange, shuffle
from decimal import Decimal
import json
import datetime

import stripe

from app.models import AccountRequest, Event, EventRegistration
from utils.utils import create_short_code
from utils.stripe import create_stripe_charge, stripe_charge_registration, stripe_charge_dues, stripe_charge_donation


# Charge Stripe Account
def stripe_charge_new(request):

    if request.is_ajax():

        token = request.POST['token_id'].strip()
        payment_type = request.POST['payment_type'].strip()
        payment_type_id = request.POST['payment_type_id'].strip()
        payment_amount = request.POST['payment_amount'].strip()
        payment_email = request.POST['payment_email'].strip()

        # to use this for more than one charge type, I will need to create a util
        # campaigns, dues, etc
        if payment_type == 'event':

            return_obj = stripe_charge_registration(
                payment_type_id = payment_type_id,
                token = token
                )

        elif payment_type == 'dues':

            return_obj = stripe_charge_dues(
                type_id = payment_type_id,
                token = token,
                amount = int(payment_amount),
                email = payment_email
            )


        elif payment_type == 'donation':

            payment_name = request.POST['payment_name'].strip()
            payment_note = request.POST['payment_note'].strip()

            return_obj = stripe_charge_donation(
                token = token,
                amount = int(payment_amount),
                name = payment_name,
                email = payment_email,
                note = payment_note
            )


        return JsonResponse(return_obj)

    else:
        return HttpResponse('is POST')

def validate_email_action(request):

    if request.is_ajax():

        email = request.POST['email'].strip()

        try:
            validate_email(email)
            email_is_valid = 'true'
        except:
            email_is_valid = ''

        return_obj = {
            'is_valid': email_is_valid
        }


        return JsonResponse(return_obj)

    else:
        return HttpResponse('')
