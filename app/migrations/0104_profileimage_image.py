# Generated by Django 2.2.5 on 2019-09-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0103_profileimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='image',
            field=models.FileField(default='profile.jpg', upload_to='documents/'),
            preserve_default=False,
        ),
    ]
