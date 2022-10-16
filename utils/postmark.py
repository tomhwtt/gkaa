from django.core.mail import send_mail

import datetime
from decouple import config
import requests
import json

from app.models import Profile, ContactRequest, Registration


def get_key():
    return config('POSTMARK_KEY')


def send_postmark_notification(subject,body):

    payload = {
        'From': 'notifications@goldenknightsalumni.org',
        'To': 'goldenknightsalumni@gmail.com ',
        'Subject': subject,
        'TextBody': body
    }

    url = 'https://api.postmarkapp.com/email'
    key = get_key()

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})

    return r

def send_schedule_email():

    # get the contact request
    registration_list = Registration.objects.filter(
        email_sent__isnull=True).exclude(
        stripe_charge_id=''
        )[:50]

    from_email = 'gkaa@goldenknightsalumni.org'

    emails_sent = 0

    for reg in registration_list:

        to_email = reg.email_address.strip()
        emails_sent += 1

        payload = {
            "From": from_email,
            "To": to_email,
            "ReplyTo": from_email,
            "TemplateAlias": "reunion-schedule",
            "TemplateModel":{

            }
        }

        url = 'https://api.postmarkapp.com/email/withTemplate'

        key = get_key()

        r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})

        reg.email_sent = datetime.datetime.now()
        reg.save()


    return emails_sent

def send_contactrequest_email(c):

    # get the contact request
    contactrequest = ContactRequest.objects.get(id=c)

    from_email = 'notifications@goldenknightsalumni.org'
    to_email = 'goldenknightsalumni@gmail.com'

    payload = {
        "From": from_email,
        "To": to_email,
        "ReplyTo": contactrequest.email_address,
        "TemplateAlias": "contact-request",
        "TemplateModel":{
            "name": contactrequest.name,
            "email": contactrequest.email_address,
            "message": contactrequest.message

        }
    }

    url = 'https://api.postmarkapp.com/email/withTemplate'
    key = get_key()

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})


    return r

def accountrequest_notification(a):

    # get the contact request
    from_email = ''
    to_email = ''

    payload = {
        "From": 'notifications@goldenknightsalumni.org',
        "To": 'goldenknightsalumni@gmail.com',
        "ReplyTo": a.email_address,
        "TemplateAlias": "account-request",
        "TemplateModel":{
            "name": a.name,
            "email": a.email_address,
            "message": a.info,
            'subject': 'GKAA Account Request [' + a.name + ']'

        }
    }

    url = 'https://api.postmarkapp.com/email/withTemplate'
    key = get_key()

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})


    return r

def send_user_account_notice(name,email):

    from_email = 'gkaa@goldenknightsalumni.org'
    to_email = email
    to_name = name

    payload = {
        "From": from_email,
        "To": to_email,
        "TemplateAlias": "user-account-notice",
        "TrackOpens": "true",
        "TemplateModel":{
            "name": name,
            'subject': 'Your GKAA User Account Info'

        }
    }

    url = 'https://api.postmarkapp.com/email/withTemplate'
    key = get_key()

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})

    return r

def send_eventregistration_email(registration):

    from_email = 'notifications@goldenknightsalumni.org'
    to_email = registration.email
    to_name = registration.name

    payload = {
        "From": from_email,
        "To": to_email,
        "ReplyTo": 'goldenknightsalumni@gmail.com',
        "TemplateAlias": "schedule",
        "TrackOpens": "true",
        "TemplateModel":{
            "name": to_name,
            'subject': 'Schedule for Reunion Weekend'

        }
    }

    url = 'https://api.postmarkapp.com/email/withTemplate'
    key = get_key()

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})

    return r

def send_event_email(messages):

    payload = {
        "Messages": messages
    }

    url = 'https://api.postmarkapp.com/email/batchWithTemplates'
    key = '2011a646-f10c-46f4-9d02-f5096dee847b'

    r = requests.post(url, json=payload, headers={'X-Postmark-Server-Token': key})

    return r
