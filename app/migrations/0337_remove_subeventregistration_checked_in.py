# Generated by Django 3.2.9 on 2021-11-30 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0336_rename_checked_in_time_subeventregistration_checked_in_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subeventregistration',
            name='checked_in',
        ),
    ]