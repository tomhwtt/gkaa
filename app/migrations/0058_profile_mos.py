# Generated by Django 2.2 on 2019-07-21 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20190721_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mos',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]