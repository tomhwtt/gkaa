from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100,blank=True)
    relationship = models.CharField(max_length=50,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def text_date(self):
        return self.date_joined.strftime('%b %-d, %Y')

    class Meta:
        ordering = ('-date_joined',)

    def __str__(self):
        return self.email
