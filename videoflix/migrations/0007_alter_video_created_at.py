# Generated by Django 4.2.7 on 2023-12-04 21:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0006_alter_video_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 4, 21, 13, 28, 289368, tzinfo=datetime.timezone.utc)),
        ),
    ]
