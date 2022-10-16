# Generated by Django 2.2 on 2019-08-26 09:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0096_highlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
    ]