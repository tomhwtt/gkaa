# Generated by Django 2.2 on 2019-04-07 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_servicedate_start_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnus',
            name='search_field',
            field=models.TextField(blank=True),
        ),
    ]
