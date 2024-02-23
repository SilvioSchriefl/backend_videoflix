import subprocess
import os


def create_thumbnail(video):
    video_path = video.file.path
    thumbnail_path = video.thumbnail.path
    cmd = ['ffmpeg', '-i', video_path, '-ss', '00:00:03.000', '-vframes', '1', thumbnail_path]
    subprocess.run(cmd, check=True)

    with open(thumbnail_path, 'rb') as f:
            video.thumbnail_file.save(os.path.basename(thumbnail_path), f, save=True)
        
