# Generated by Django 3.0.4 on 2021-11-15 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0289_auto_20211114_1201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrytype',
            options={'ordering': ('sort_order',)},
        ),
        migrations.AddField(
            model_name='entrytype',
            name='sort_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
