from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user = self.create_user(email, password, **extra_fields)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    password_reset_token_used = models.BooleanField(default=False)
    user_name = models.CharField(max_length=100, default='', blank=False, null=False)
    watchlist = models.JSONField(default=list, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    

    def __str__(self):
        return self.user_name
    
class Video(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description  = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='videos', max_length=100, blank=True)
    thumbnail = models.FileField(upload_to='thumbnails', blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    

    
    def __str__(self):
        return  self.title
    
    def video_id(self):			
        return self.id
    

    
   

      
    




   
        

    


