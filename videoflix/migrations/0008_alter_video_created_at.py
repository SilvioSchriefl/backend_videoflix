# Generated by Django 4.2.7 on 2023-12-04 21:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0007_alter_video_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
