# Generated by Django 2.2 on 2019-04-01 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_teamstarttwo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Honorary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]