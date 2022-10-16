# Generated by Django 2.2 on 2019-08-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_auto_20190722_0727'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='army_highlights',
            field=models.TextField(default='army highlight'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='civilian_highlights',
            field=models.TextField(default='civilian highlight'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='current_status',
            field=models.TextField(default='current status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='deceased',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='team_highlights',
            field=models.TextField(default='team highlights'),
            preserve_default=False,
        ),
    ]