# Generated by Django 2.2 on 2019-04-02 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alumnus_hide_from_roster'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email_address', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
