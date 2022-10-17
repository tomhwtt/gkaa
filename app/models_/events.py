from django.db import models
from django.db.models import Sum, Q
import uuid
import datetime

from decimal import Decimal

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    cutoff_date = models.DateTimeField()
    door_price = models.DecimalField(max_digits=10, decimal_places=2)
    short_code = models.SlugField()
    test_mode = models.BooleanField(default=True)
    closed_message = models.CharField(max_length=60)

    def is_closed(self):

        if datetime.datetime.now() > self.cutoff_date:
            return True
        else:
            return False

    def __str__(self):
        return self.name

class SubEvent(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def num_attendees(self):

        num = self.subeventregistration_set.filter(
            eventregistration__cancelled = 0,
            eventregistration__comped = False
        ).exclude(
            eventregistration__stripe_charge_id = '',
        ).aggregate(
            quantity=Sum('quantity')
        )

        return num['quantity']

    def __str__(self):
        return self.name

class SubEventPricing(models.Model):
    subevent = models.ForeignKey(SubEvent,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    add_on_pricing = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    alumnus_choice = 1
    current_choice = 2
    honorary_choice = 3
    other_choice = 4
    type_choices = (
        (alumnus_choice, 'Alumnus'),
        (current_choice, 'Current'),
        (honorary_choice, 'Honorary'),
        (other_choice, 'Other')
    )
    type = models.IntegerField(choices=type_choices,default=alumnus_choice)
    quantity = models.PositiveIntegerField()
    free_with_dues = models.BooleanField(default=False)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return str(self.amount)

class EventPricing(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cutoff_date = models.DateField()
    none_choice = 0
    alumnus_choice = 1
    current_choice = 2
    honorary_choice = 3
    other_choice = 4
    type_choices = (
        (none_choice, 'None'),
        (alumnus_choice, 'Alumnus'),
        (current_choice, 'Current'),
        (honorary_choice, 'Honorary'),
        (other_choice, 'Other')
    )
    type = models.IntegerField(choices=type_choices,default=none_choice)


    class Meta:
        ordering = ('type','cutoff_date',)

    def __str__(self):
        return str(self.amount)

class EventRegistration(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150,blank=True)
    last_name =  models.CharField(max_length=150,blank=True)
    email = models.EmailField()
    short_code = models.CharField(max_length=8)
    date = models.DateTimeField(auto_now_add=True)
    alumnus_choice = 1
    current_choice = 2
    honorary_choice = 3
    other_choice = 4
    type_choices = (
        (alumnus_choice, 'Alumnus'),
        (current_choice, 'Current'),
        (honorary_choice, 'Honorary'),
        (other_choice, 'Other')
    )
    type = models.IntegerField(choices=type_choices, default=alumnus_choice)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    stripe_charge_id = models.CharField(max_length=32,blank=True)
    dues_added = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    comped = models.BooleanField(default=False)

    def email_display(self):

        #split the email address
        username = self.email.split('@')[0]
        domain_name = self.email.split('@')[1]

        try:

            if len(username) > 5:
                username = username[:2] + '***' + username[4:]

            safe_email = username + '@' + domain_name

        except:

            safe_email = self.email

        return safe_email

    def cart(self):

        subeventregistration_set = self.subeventregistration_set.all()

        dues_paid = check_dues_by_email(email=self.email)

        add_dues = False # by default
        cart_items = []
        cart_total = 0

        # for SubEventRegistration in SubEventRegistration Set
        for sub in subeventregistration_set:

            # I need to know if they have already bought tickets for this SubEvent
            # exclude this SubEventRegistration
            existing_tickets = SubEventRegistration.objects.filter(
                eventregistration__email = self.email,
                subevent = sub.subevent,
                quantity__gt=0
            ).exclude(
                Q(pk=sub.pk) |
                Q(eventregistration__stripe_charge_id = '')
            )

            # set the number of tickets
            num_existing_tickets = 0

            # increment num_tickets
            # I could use SUM for this (update later?)
            for ticket in existing_tickets:
                num_existing_tickets += ticket.quantity

            # get the SubEventPricing
            pricing = SubEventPricing.objects.get(
                subevent = sub.subevent,
                type = self.type
            )

            # if they have already bought tickets, these are all add_on_pricing
            if sub.quantity and existing_tickets:
                total = sub.quantity * pricing.add_on_pricing

            # if they have not bought tickets yet, they get charged
            # the min quantity for the SubEvent PLUS
            # any above and beyond that * add_on_pricing
            elif sub.quantity and not existing_tickets:

                # if they want more than the minimum for this SubEvent
                # we need to know how many are leftover
                if sub.quantity > pricing.quantity:
                    this_lefotver = sub.quantity - pricing.quantity

                # if they want the minimum number or fewer
                # set this to Zero so it is not a negative number
                else:
                    this_lefotver = 0


                # they get charged the the min quantity for the SubEvent (pricing.amount)
                # PLUS
                # any above and beyond that * add_on_pricing
                total = (
                    pricing.amount +
                    (this_lefotver * pricing.add_on_pricing)
                )

            # if not sub.quantity (they do not want tickets)
            else:
                total = 0

            # if they have not bought tickets yet and have paid their dues
            # are they eligible for free tickets?
            if not existing_tickets and dues_paid and pricing.free_with_dues:
                total -= 50

            # lastly, if the total is less than 0, make it zero
            if total < 0:
                total = 0

            cart_total += total

            # if they have not bought tickets and this is free_with_dues pricing
            # add their dues once they pay
            if (
                self.type == 1 and
                not dues_paid and
                pricing.free_with_dues
                ):

                add_dues = True

            cart_obj = {
                'name': sub.subevent.name,
                'quantity': sub.quantity,
                'total': total,
                'existing_tickets': num_existing_tickets
            }

            cart_items.append(cart_obj)

        cart = {
            'items': cart_items,
            'total': cart_total,
            'add_dues': add_dues,
            'dues_paid': 'are dues paid'
        }

        return cart

    def __str__(self):
        return self.email

class SubEventRegistration(models.Model):
    eventregistration = models.ForeignKey(EventRegistration,on_delete=models.CASCADE)
    subevent = models.ForeignKey(SubEvent,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    checked_in_date = models.DateTimeField(null=True)
