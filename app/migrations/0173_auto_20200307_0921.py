# Generated by Django 2.2.5 on 2020-03-07 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0172_auto_20200307_0635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profilestory',
            options={'ordering': ('-id',)},
        ),
    ]
