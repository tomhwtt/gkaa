# Generated by Django 3.0.4 on 2021-08-03 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0256_auto_20210803_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubEventRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('each', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('eventregistration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.EventRegistration')),
            ],
        ),
    ]