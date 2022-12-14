# Generated by Django 2.2 on 2019-07-21 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_remove_registration_dues_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(blank=True, max_length=5)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('nickname', models.CharField(blank=True, max_length=50)),
                ('aka', models.CharField(blank=True, max_length=50, verbose_name='AKA')),
                ('old_id', models.PositiveSmallIntegerField(default=0, editable=False)),
            ],
        ),
    ]
