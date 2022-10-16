# Generated by Django 3.0.4 on 2021-11-14 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0285_auto_20211112_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileentry',
            name='text',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='ProfileEntryExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example', models.CharField(max_length=150)),
                ('profileentry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ProfileEntry')),
            ],
        ),
    ]
