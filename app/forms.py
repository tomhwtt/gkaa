
from django.forms import ModelForm

# import models
from app.models import Profile, ProfileImage, AccountRequest
from users.models import CustomUser


class NewProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            'rank','first_name','last_name','nickname',
            'aka','type'
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            'rank','first_name','last_name','nickname',
            'aka','home_city','home_state', 'd_number', 'gkas_year', 'mos',
            'comments', 'current_status'
        )


class ProfileImageForm(ModelForm):
    class Meta:
        model = ProfileImage
        fields = ('image',)

class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'name','email'
        )
