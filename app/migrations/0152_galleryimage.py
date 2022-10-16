# Generated by Django 2.2.5 on 2019-11-27 06:53

import app.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0151_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(blank=True)),
                ('credit', models.CharField(blank=True, max_length=150)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.FileField()),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Gallery')),
            ],
        ),
    ]