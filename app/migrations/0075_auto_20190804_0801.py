# Generated by Django 2.2 on 2019-08-04 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0074_olduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.IntegerField(choices=[(1, 'Alumnus/Alumnae'), (2, 'Current Team Member'), (3, 'Honorary GK'), (4, 'Other')]),
        ),
    ]
