import subprocess
import os

def convert_480p(source):
    target = os.path.splitext(source)[0] + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"' .format(source, target)
    subprocess.run(cmd)
    
def convert_720p(source):
    target = os.path.splitext(source)[0] + '_720p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"' .format(source, target)
    subprocess.run(cmd)
    
def convert_1080p(source):
    target = os.path.splitext(source)[0] + '_1080p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"' .format(source, target)
    subprocess.run(cmd)