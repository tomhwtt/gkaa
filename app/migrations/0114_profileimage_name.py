# Generated by Django 2.2.5 on 2019-10-04 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0113_auto_20191004_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='name',
            field=models.CharField(default='name.jpg', max_length=250),
            preserve_default=False,
        ),
    ]
