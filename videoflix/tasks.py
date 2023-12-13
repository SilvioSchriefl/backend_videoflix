import subprocess
import os
from .models import Thumbnail

def convert_480p_and_update_model(source, video_instance):
    base_path, file_name = os.path.split(source)
    file_name_without_extension, extension = os.path.splitext(file_name)

    target = os.path.join(base_path, f"{file_name_without_extension}_480p.mp4")

    cmd = ['ffmpeg', '-i', source ,'-vf', 'scale=480:-1', target]

    try:
        subprocess.check_call(cmd)
        print(f"Konvertierung zu 480p erfolgreich: {source}")

        video_instance.file_480p.name = f"videos/{file_name_without_extension}_480p.mp4"
        video_instance.save()

        print(f"Video-Modell aktualisiert mit 480p-Datei: {video_instance.file_480p.name}")

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Konvertierung zu 480p: {e}")
        
def create_thumbnail(source, video_instance):
    base_path, file_name = os.path.split(source)
    file_name_without_extension, extension = os.path.splitext(file_name)

    thumbnail_name = None  # Initialisiere die Variable hier

    try:
        thumbnail_name = f"{file_name_without_extension}_thumbnail.png"
        thumbnail_path = os.path.join(base_path, thumbnail_name)

        cmd = ['ffmpeg', '-i', source, '-ss', '00:00:05', '-vframes', '1', thumbnail_path]

        subprocess.run(cmd, capture_output=True, check=True)
        print(f"Thumbnail erfolgreich erstellt: {thumbnail_name}")

        # Hier erstellen wir ein neues Thumbnail-Objekt
        thumbnail = Thumbnail()
        thumbnail.title = video_instance.title
        thumbnail.category = "Default"  # Hier kannst du die Kategorie anpassen oder aus dem Video-Modell übernehmen
        thumbnail.video = video_instance
        thumbnail.thumbnail.save(thumbnail_name, open(thumbnail_path, 'rb'))

        # Lösche das temporäre Thumbnail-File
        os.remove(thumbnail_path)

        print(f"Thumbnail erfolgreich im Modell Thumbnail gespeichert.")

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der Thumbnail-Erstellung: {e}")

        # Handle den Fehler hier weiter, wenn nötig

    # Wenn es außerhalb des try-except-Blocks benötigt wird, kann thumbnail_name hier weiterverwendet werden.
    return thumbnail_name