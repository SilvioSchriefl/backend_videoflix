# Generated by Django 4.2.7 on 2024-02-24 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0002_alter_video_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='file_480p',
            field=models.FileField(blank=True, upload_to='videos'),
        ),
    ]
