
from django.forms import ModelForm
from app.models import Profile, AccountRequest, ProfileImage


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            'rank','first_name','middle_name','last_name','nickname','aka',
            'home_city','home_state','d_number','gkas_year','mos'
            )

class AccountRequestForm(ModelForm):
    class Meta:
        model = AccountRequest
        fields = ('name','email_address','info')
