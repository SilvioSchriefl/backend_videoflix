# Generated by Django 4.2.7 on 2023-12-03 23:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0004_rename_titel_video_title_video_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2023, 12, 4)),
        ),
    ]