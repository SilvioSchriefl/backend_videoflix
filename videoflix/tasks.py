import subprocess
import os
from django.core.files import File


def create_thumbnail(video):
    video_path = video.file.path
    thumbnail_path = video + '.jpg'
    cmd = ['ffmpeg', '-i', video_path, '-ss', '00:00:03.000', '-vframes', '1', thumbnail_path]
    subprocess.run(cmd, check=True)

       
    video.thumbnail.save(thumbnail_path, File(open(thumbnail_path, 'rb')), save=False)
    video.save()

 
        
