# Generated by Django 2.2.5 on 2019-10-16 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0125_auto_20191016_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='deceased',
            new_name='deceased_date',
        ),
    ]