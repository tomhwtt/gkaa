# Generated by Django 2.2 on 2019-08-06 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0090_auto_20190806_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comments',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
