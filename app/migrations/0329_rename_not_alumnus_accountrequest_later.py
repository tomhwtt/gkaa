# Generated by Django 3.2.9 on 2021-11-27 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0328_accountrequest_not_alumnus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountrequest',
            old_name='not_alumnus',
            new_name='later',
        ),
    ]
