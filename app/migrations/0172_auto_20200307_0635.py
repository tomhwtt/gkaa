# Generated by Django 2.2.5 on 2020-03-07 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0171_story'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Story',
            new_name='ProfileStory',
        ),
    ]