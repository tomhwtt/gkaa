# Generated by Django 2.2.5 on 2019-11-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0145_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_address', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('member_id', models.CharField(max_length=15)),
                ('notes', models.TextField()),
            ],
        ),
    ]