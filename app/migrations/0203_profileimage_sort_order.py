# Generated by Django 2.2.5 on 2020-03-13 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0202_profileentry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='sort_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]