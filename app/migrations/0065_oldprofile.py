# Generated by Django 2.2 on 2019-08-01 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0064_auto_20190801_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField()),
                ('member_id', models.PositiveIntegerField()),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150)),
                ('nickname', models.CharField(blank=True, max_length=150)),
                ('aka', models.CharField(blank=True, max_length=150)),
                ('rank', models.CharField(blank=True, max_length=50)),
                ('hometown', models.CharField(blank=True, max_length=50)),
                ('email_address', models.EmailField(max_length=250)),
                ('deceased', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('type', models.CharField(blank=True, max_length=50)),
                ('army_start_date', models.CharField(blank=True, max_length=50)),
                ('army_end_date', models.CharField(blank=True, max_length=50)),
                ('team_start_one', models.CharField(blank=True, max_length=50)),
                ('team_start_two', models.CharField(blank=True, max_length=50)),
                ('team_end_one', models.CharField(blank=True, max_length=50)),
                ('team_end_two', models.CharField(blank=True, max_length=50)),
                ('goy1', models.CharField(blank=True, max_length=50)),
                ('goy2', models.CharField(blank=True, max_length=50)),
                ('aoy1', models.CharField(blank=True, max_length=50)),
                ('aoy2', models.CharField(blank=True, max_length=50)),
                ('army_jobs', models.TextField()),
                ('team_jobs', models.TextField()),
                ('army_beats', models.TextField()),
                ('team_beats', models.TextField()),
                ('civilian_beats', models.TextField()),
                ('awards', models.TextField()),
                ('comments', models.TextField()),
                ('notes', models.TextField()),
                ('license', models.TextField()),
                ('current_status', models.TextField()),
                ('coy1', models.CharField(blank=True, max_length=50)),
                ('coy2', models.CharField(blank=True, max_length=50)),
                ('poy1', models.CharField(blank=True, max_length=50)),
                ('poy2', models.CharField(blank=True, max_length=50)),
                ('hgk', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
