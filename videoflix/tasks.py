import subprocess
import os


def create_thumbnail(video):
    video_path = video.file.path
    thumbnail_path = video.thumbnaile.path
    cmd = ['ffmpeg', '-i', video_path, '-ss', '00:00:03.000', '-vframes', '1', thumbnail_path]
    subprocess.run(cmd)

        
