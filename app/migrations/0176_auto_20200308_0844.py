# Generated by Django 2.2.5 on 2020-03-08 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0175_profilestory_short_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='text',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='license',
            name='text',
            field=models.CharField(max_length=250),
        ),
        migrations.CreateModel(
            name='ArmyJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Profile')),
            ],
        ),
    ]
