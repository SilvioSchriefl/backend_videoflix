from videoflix.tasks import convert_480p_and_update_model
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import os 
import django_rq


