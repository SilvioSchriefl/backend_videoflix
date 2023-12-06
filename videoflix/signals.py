from videoflix.tasks import convert_480p
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import os 
import django_rq

@receiver(post_save, sender=Video)

def video_post_save(sender, instance, created, **kwargs):
    if created:
        convert_480p(instance.file.path)
        #queue = django_rq.get_queue('default', autocommit=True)
        #queue.enqueue(convert_480p, instance.file.path)
        #queue.enqueue(convert_720p, instance.file.path)
        #queue.enqueue(convert_1080p, instance.file.path)
        
@receiver(post_delete, sender=Video)
    
def video_post_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.exists(instance.file.path):
            os.remove(instance.file.path)
            os.remove(instance.file_480p.path)
            os.remove(instance.thumbnail.path)