# Generated by Django 2.2.5 on 2020-03-14 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0206_auto_20200313_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='name',
            field=models.CharField(default='imagename.jpg', max_length=20),
            preserve_default=False,
        ),
    ]
