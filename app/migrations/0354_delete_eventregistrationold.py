# Generated by Django 3.2.13 on 2022-05-21 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0353_alter_attendee_event'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventRegistrationOld',
        ),
    ]
