# Generated by Django 3.2.9 on 2021-11-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0319_remove_galleryimage_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='roster_image',
            field=models.BooleanField(default=False),
        ),
    ]
