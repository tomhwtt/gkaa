# Generated by Django 3.0.4 on 2020-03-16 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0218_auto_20200316_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileentry',
            name='details',
            field=models.TextField(blank=True),
        ),
    ]
