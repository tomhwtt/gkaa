# Generated by Django 3.0.4 on 2021-08-04 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0266_subeventpricing_free_with_dues'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='app.Event'),
            preserve_default=False,
        ),
    ]