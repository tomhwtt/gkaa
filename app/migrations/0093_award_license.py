# Generated by Django 2.2 on 2019-08-07 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0092_auto_20190806_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
    ]
