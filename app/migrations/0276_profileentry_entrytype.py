# Generated by Django 3.0.4 on 2021-11-04 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0275_auto_20211104_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileentry',
            name='entrytype',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='app.EntryType'),
            preserve_default=False,
        ),
    ]
