from rest_framework import serializers
from .models import CustomUser, Video, Thumbnail
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'user_name', 'email_confirmed')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class ResetPasswordSerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ('email',)
        
class SetNewPasswordSerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ('password', 'user_id',)
        extra_kwargs = {'password': {'write_only': True}}
        
class GetPreviewVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ('file_480p',)
        
class GetThumbnailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Thumbnail
        fields = '__all__'
        
class GetVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ('file',)