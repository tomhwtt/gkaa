# Generated by Django 2.2.5 on 2019-11-02 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0135_auto_20191101_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
