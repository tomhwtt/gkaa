# Generated by Django 3.2.9 on 2021-11-22 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0317_galleryimage_old_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='galleryimageholder',
            options={'ordering': ('id',)},
        ),
    ]
