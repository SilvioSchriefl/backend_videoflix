import subprocess
import os

def convert_480p_and_update_model(source, video_instance):
    base_path, file_name = os.path.split(source)
    file_name_without_extension, extension = os.path.splitext(file_name)

    target = os.path.join(base_path, f"{file_name_without_extension}_480p.mp4")

    cmd = [
        'ffmpeg',
        '-i', source,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]

    try:
        subprocess.check_call(cmd)
        print(f"Konvertierung zu 480p erfolgreich: {source}")

        video_instance.file_480p.name = f"videos/480p/{file_name_without_extension}_480p.mp4"
        video_instance.save()

        print(f"Video-Modell aktualisiert mit 480p-Datei: {video_instance.file_480p.name}")

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Konvertierung zu 480p: {e}")