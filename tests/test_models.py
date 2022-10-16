from pytest import mark
import datetime

from app.models import Profile, DuesPayment

@mark.django_db
class ProfileTests:

    def test_profile_string(self,profile):
        assert profile.__str__() == 'Knight, Joe'

    def test_dues_paid_returns_false_when_no_dues_payments_found(self,profile):
        assert profile.dues_paid() == False

    def test_dues_paid_returns_true_when_dues_paid_for_current_year(self):

        profile = Profile.objects.create(
            first_name = 'Joe',
            last_name = 'Knight'
        )

        payment = DuesPayment.objects.create(
            profile = profile,
            name = 'Joe Knight',
            email = 'joe@gmail.com',
            amount = 50.00,
            stripe_charge_id = 'ch_3JPRSuLzCvCwRY0K0DJUNeue',
            year = datetime.datetime.now().year
        )

        assert profile.dues_paid() is True

    def test_dues_paid_returns_true_when_dues_paid_for_next_year(self):

        profile = Profile.objects.create(
            first_name = 'Joe',
            last_name = 'Knight'
        )

        next_year = datetime.datetime.now() + datetime.timedelta(days=369)

        payment = DuesPayment.objects.create(
            profile = profile,
            name = 'Joe Knight',
            email = 'joe@gmail.com',
            amount = 50.00,
            stripe_charge_id = 'ch_3JPRSuLzCvCwRY0K0DJUNeue',
            year = next_year.year
        )

        assert profile.dues_paid() is True

    def test_dues_paid_returns_false_when_dues_not_paid_for_current_year(self):

        profile = Profile.objects.create(
            first_name = 'Joe',
            last_name = 'Knight'
        )

        last_year = datetime.datetime.now() - datetime.timedelta(days=369)

        payment = DuesPayment.objects.create(
            profile = profile,
            name = 'Joe Knight',
            email = 'joe@gmail.com',
            amount = 50.00,
            stripe_charge_id = 'ch_3JPRSuLzCvCwRY0K0DJUNeue',
            year = last_year.year
        )

        assert profile.dues_paid() is False

    # def test_dues_paid_returns_false_when_dues_not_paid_this_year(self,profile,dues_payment):
    #     dues_year = datetime.datetime.now() - datetime.timedelta(days=400)
    #     dues_payment.year = int(dues_year.year)
    #     assert profile.dues_paid() == False

@mark.django_db
class EventTests:

    def test_event_string(self,event):
        assert event.__str__() == 'Annual Reunion'

    def test_is_closed_returns_true_when_cutoff_date_is_now(self,event):
        assert event.is_closed() is True

    def test_is_closed_returns_true_when_cutoff_date_is_past(self,event):
        event.cutoff_date = datetime.datetime.now() - datetime.timedelta(seconds=60)
        assert event.is_closed() is True

    def test_is_closed_returns_false_when_cutoff_date_is_future(self,event):
        event.cutoff_date = datetime.datetime.now() + datetime.timedelta(seconds=60)
        assert event.is_closed() is False

@mark.django_db
class PaymentTests:

    def test_dues_payment_string(self,dues_payment):
        assert dues_payment.__str__() == 'joe_knight@gmail.com'

    def test_dues_payment_returns_correct_total(self,dues_payment):
        assert dues_payment.total() == 50.00

    def test_dues_payment_returns_correct_text_date(self,dues_payment):
        dues_payment.date = datetime.datetime(2022,5,22,10,36,00)
        assert dues_payment.text_date() == 'May 22, 2022 @ 10:36AM'

    def test_donation_payment_string(self,donation_payment):
        assert donation_payment.__str__() == 'sally@gmail.com'

    def test_donation_payment_returns_correct_amount(self,donation_payment):
        assert donation_payment.total() == 350.00
