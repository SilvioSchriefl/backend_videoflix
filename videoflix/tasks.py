import subprocess
import os
from django.core.files.base import ContentFile


def create_thumbnail(video):
 
    thumbnail_path = video + '.jpg'
    cmd = ['ffmpeg', '-i', video, '-ss', '00:00:03.000', '-vframes', '1', thumbnail_path]
    subprocess.run(cmd, check=True)

    with open(thumbnail_path, 'rb') as f:
        thumbnail_name = os.path.basename(thumbnail_path)
        video.thumbnail.save(thumbnail_name, ContentFile(f.read()), save=True)
        
