# Generated by Django 3.0.4 on 2020-08-12 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0248_event_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='short_code',
            field=models.SlugField(),
        ),
    ]