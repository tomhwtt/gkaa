# Generated by Django 3.0.4 on 2020-09-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0249_auto_20200812_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='duespayment',
            name='year',
            field=models.PositiveIntegerField(default=2019),
            preserve_default=False,
        ),
    ]