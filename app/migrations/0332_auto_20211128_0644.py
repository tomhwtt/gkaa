# Generated by Django 3.2.9 on 2021-11-28 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0331_accountrequest_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrequest',
            name='complete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='accountrequest',
            name='pending_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]