# Generated by Django 2.2 on 2019-08-27 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0099_auto_20190826_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlight',
            name='type',
            field=models.IntegerField(choices=[(0, 'Team Highlight'), (1, 'Army Highlight'), (2, 'Civilian Highlight'), (3, 'Licenses & Ratings'), (4, 'Awards & Badges')]),
        ),
    ]