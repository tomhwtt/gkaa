# Generated by Django 2.2.5 on 2019-10-04 07:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0114_profileimage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
