# Generated by Django 2.2.5 on 2019-10-06 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0121_profile_short_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='short_code',
            field=models.CharField(max_length=12),
        ),
    ]
