# Generated by Django 3.0.4 on 2020-08-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0247_event_test_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
    ]