# Generated by Django 2.2.5 on 2019-11-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0155_oldgalleryimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldgalleryimage',
            name='year',
            field=models.CharField(blank=True, default='', max_length=150),
            preserve_default=False,
        ),
    ]
