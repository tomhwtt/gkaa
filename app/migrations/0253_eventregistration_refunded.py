# Generated by Django 3.0.4 on 2020-11-19 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0252_profileimage_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
    ]
