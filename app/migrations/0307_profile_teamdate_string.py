# Generated by Django 3.2.9 on 2021-11-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0306_profilefilter_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='teamdate_string',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]