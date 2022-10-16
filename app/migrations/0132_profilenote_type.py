# Generated by Django 2.2.5 on 2019-10-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0131_profilenote'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilenote',
            name='type',
            field=models.IntegerField(choices=[(1, 'In House'), (2, 'Public/Website')], default=1),
        ),
    ]