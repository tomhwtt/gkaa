# Generated by Django 3.0.4 on 2020-03-15 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0212_profile_url_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileentry',
            name='date_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
