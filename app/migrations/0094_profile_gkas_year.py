# Generated by Django 2.2 on 2019-08-07 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0093_award_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gkas_year',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]