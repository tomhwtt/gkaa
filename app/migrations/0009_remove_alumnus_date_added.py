# Generated by Django 2.2 on 2019-04-01 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20190401_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumnus',
            name='date_added',
        ),
    ]
