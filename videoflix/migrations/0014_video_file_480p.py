# Generated by Django 4.2.7 on 2023-12-06 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix', '0013_thumbnail_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='file_480p',
            field=models.FileField(blank=True, upload_to='videos/480p'),
        ),
    ]
