# Generated by Django 3.2.13 on 2022-05-21 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0351_rename_event_attendee_revent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendee',
            old_name='revent',
            new_name='event',
        ),
    ]
