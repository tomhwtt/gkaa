# Generated by Django 2.2.5 on 2019-11-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0157_oldgalleryimage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldgalleryimage',
            name='gallery',
            field=models.PositiveIntegerField(default=0),
        ),
    ]