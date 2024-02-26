import subprocess
import os
from django.core.files import File


def create_thumbnail(video):
    video_path = video.file.path
    thumbnail_path = video.title + '.jpg'

    try:
        cmd = ['ffmpeg', '-i', video_path, '-ss', '00:00:05.000', '-vframes', '1', thumbnail_path]
        subprocess.run(cmd, check=True)
        video.thumbnail.save(thumbnail_path, File(open(thumbnail_path, 'rb')), save=False)
        video.save()
        os.remove(thumbnail_path)

    except subprocess.CalledProcessError as e:
       
        thumbnail_path = './media/placeholder.png'
        video.thumbnail.save('./placeholder.png', File(open(thumbnail_path, 'rb')), save=False)
        video.save()


def create_480p(video):
    video_path = video.file.path
    video_480p_path = video.title + '_480p.mp4'
    
    try:
        cmd = ['ffmpeg', '-i', video_path, '-vf', 'scale=-2:480', video_480p_path]
        subprocess.run(cmd, check=True)
        video.file_480p.save(video_480p_path, File(open(video_480p_path, 'rb')), save=False)
        video.save()
        os.remove(video_480p_path)

    except subprocess.CalledProcessError as e:
        print(e)

 
        
