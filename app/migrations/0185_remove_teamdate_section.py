# Generated by Django 2.2.5 on 2020-03-12 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0184_auto_20200310_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamdate',
            name='section',
        ),
    ]
