# Generated by Django 2.2 on 2019-07-13 08:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
