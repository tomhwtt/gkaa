# Generated by Django 2.2 on 2019-08-05 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0083_remove_profile_deceased_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='army_highlights_old',
            field=models.TextField(blank=True),
        ),
    ]