# Generated by Django 3.0.4 on 2021-11-14 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0286_auto_20211114_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileentryexample',
            name='profileentry',
        ),
    ]
