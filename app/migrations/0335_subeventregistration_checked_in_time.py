# Generated by Django 3.2.9 on 2021-11-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0334_subeventregistration_checked_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='subeventregistration',
            name='checked_in_time',
            field=models.DateTimeField(null=True),
        ),
    ]
