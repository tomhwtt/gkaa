# Generated by Django 3.2.9 on 2021-11-30 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0335_subeventregistration_checked_in_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subeventregistration',
            old_name='checked_in_time',
            new_name='checked_in_date',
        ),
    ]