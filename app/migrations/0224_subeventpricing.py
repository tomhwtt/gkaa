# Generated by Django 3.0.4 on 2020-08-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0223_auto_20200803_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubEventPricing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SubEvent')),
            ],
        ),
    ]
