from videoflix.tasks import convert_480p_and_update_model, create_thumbnail
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import os 
import django_rq


@receiver(post_save, sender=Video)
def video_pre_save(sender, instance, **kwargs): 
    created = kwargs.get('created', False)
    if created:
        convert_480p_and_update_model(instance.file.path, instance)
        create_thumbnail(instance.file.path, instance)
        #queue = django_rq.get_queue('default', autocommit=True)
        #queue.enqueue(convert_480p, instance.file.path)
        #queue.enqueue(convert_720p, instance.file.path)
        #queue.enqueue(convert_1080p, instance.file.path)
        
@receiver(post_delete, sender=Video)
    
def video_post_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.exists(instance.file.path):
            os.remove(instance.file.path)