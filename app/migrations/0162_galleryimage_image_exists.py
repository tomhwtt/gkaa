# Generated by Django 2.2.5 on 2019-11-28 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0161_remove_galleryimage_has_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='image_exists',
            field=models.BooleanField(default=False),
        ),
    ]
