# Generated by Django 2.2.5 on 2019-10-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0124_oldhighlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='deceased_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='oldhighlight',
            name='type',
            field=models.IntegerField(choices=[(1, 'Team Highlight'), (2, 'Army Highlight'), (3, 'Civilian Highlight'), (4, 'Current Status')]),
        ),
    ]
