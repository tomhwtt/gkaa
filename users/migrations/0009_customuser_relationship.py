# Generated by Django 2.2.5 on 2019-11-20 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190803_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='relationship',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
