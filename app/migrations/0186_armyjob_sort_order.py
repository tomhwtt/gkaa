# Generated by Django 2.2.5 on 2020-03-12 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0185_remove_teamdate_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='armyjob',
            name='sort_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
