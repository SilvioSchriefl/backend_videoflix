import subprocess
import os

def convert_480p(source):
    target = os.path.splitext(source)[0] + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"' .format(source, target)
    subprocess.run(cmd)