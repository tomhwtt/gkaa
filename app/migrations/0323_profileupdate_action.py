# Generated by Django 3.2.9 on 2021-11-26 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0322_profileupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileupdate',
            name='action',
            field=models.CharField(default='profile edit', max_length=250),
            preserve_default=False,
        ),
    ]
