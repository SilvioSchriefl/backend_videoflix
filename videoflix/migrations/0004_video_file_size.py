# Generated by Django 4.2.7 on 2024-02-24 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0003_video_file_480p'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='file_size',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]