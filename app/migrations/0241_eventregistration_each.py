# Generated by Django 3.0.4 on 2020-08-12 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0240_eventregistration_add_dues'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='each',
            field=models.DecimalField(decimal_places=2, default=25, max_digits=10),
            preserve_default=False,
        ),
    ]