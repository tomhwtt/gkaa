# Generated by Django 2.2.5 on 2019-11-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0159_oldgalleryimage_transferred'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='has_image',
            field=models.BooleanField(default=False),
        ),
    ]