# Generated by Django 2.2.5 on 2019-11-27 07:15

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0152_galleryimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='old_id',
            field=models.CharField(default='old-id', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.FileField(),
        ),
    ]