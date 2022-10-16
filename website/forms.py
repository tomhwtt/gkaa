from django.forms import ModelForm


from app.models import DuesPayment, DonationPayment, ContactRequest

class DuesPaymentForm(ModelForm):
    class Meta:
        model = DuesPayment
        exclude = ('stripe_charge_id','amount','donation')

class DonationPaymentForm(ModelForm):
    class Meta:
        model = DonationPayment
        exclude = ('stripe_charge_id','amount')

class ContactRequestForm(ModelForm):
    class Meta:
        model = ContactRequest
        fields = ('name','email_address','message')
