# Generated by Django 3.0.4 on 2020-08-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0245_event_cutoff_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='door_price',
            field=models.DecimalField(decimal_places=2, default=50.0, max_digits=10),
            preserve_default=False,
        ),
    ]
