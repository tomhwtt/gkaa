# Generated by Django 3.0.4 on 2021-11-15 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0294_auto_20211115_1400'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profilecomment',
            options={'ordering': ('date',)},
        ),
    ]
