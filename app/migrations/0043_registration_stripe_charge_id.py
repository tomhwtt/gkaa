# Generated by Django 2.2 on 2019-07-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20190715_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='stripe_charge_id',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
