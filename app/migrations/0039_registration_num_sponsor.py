# Generated by Django 2.2 on 2019-07-13 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_registrationguest_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='num_sponsor',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
