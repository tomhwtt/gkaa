# Generated by Django 2.2.5 on 2020-03-09 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0180_profile_temp_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_thumbnail',
            field=models.BooleanField(default=False),
        ),
    ]