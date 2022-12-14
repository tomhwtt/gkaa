# Generated by Django 2.2 on 2019-04-01 22:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuesPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=100)),
                ('date', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('donation', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('stripe_charge_id', models.CharField(max_length=32)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
            ],
        ),
    ]
