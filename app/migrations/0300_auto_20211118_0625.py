# Generated by Django 3.0.4 on 2021-11-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0299_auto_20211118_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrequestnote',
            name='reminder_date',
            field=models.DateField(null=True),
        ),
    ]