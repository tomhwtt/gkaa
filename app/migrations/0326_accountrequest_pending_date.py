# Generated by Django 3.2.9 on 2021-11-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0325_accountrequest_pending_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountrequest',
            name='pending_date',
            field=models.DateTimeField(null=True),
        ),
    ]
