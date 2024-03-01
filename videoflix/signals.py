

from videoflix.tasks import create_thumbnail, create_480p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import os 
import django_rq

@receiver(post_delete, sender=Video)
def delete_video_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)

    if instance.file_480p and os.path.isfile(instance.file_480p.path):
        os.remove(instance.file_480p.path)

@receiver(post_save, sender=Video)
def save_video(instance, created, **kwargs):
    if created:
        create_thumbnail(instance)
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(create_480p, instance)
        
      