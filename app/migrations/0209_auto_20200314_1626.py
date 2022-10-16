# Generated by Django 3.0.4 on 2020-03-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0208_remove_oldhighlight_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldhighlight',
            name='date_delete',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='oldhighlight',
            name='title',
            field=models.CharField(default='title', max_length=50),
            preserve_default=False,
        ),
    ]