# Generated by Django 3.0.4 on 2020-08-11 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0231_subeventregistration_short_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SubEventRegistration')),
            ],
        ),
    ]