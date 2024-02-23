

from videoflix.tasks import create_thumbnail
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

@receiver(post_save, sender=Video)
def save_video(instance, created, **kwargs):
    if created:
        rq_job = django_rq.enqueue(create_thumbnail, instance)
        instance.thumbnail = rq_job.result