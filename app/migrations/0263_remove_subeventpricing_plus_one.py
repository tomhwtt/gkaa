# Generated by Django 3.0.4 on 2021-08-03 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0262_subeventpricing_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subeventpricing',
            name='plus_one',
        ),
    ]
