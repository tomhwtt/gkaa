# Generated by Django 2.2.5 on 2019-11-25 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_customuser_keep_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='keep_account',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='profile_id',
        ),
    ]
