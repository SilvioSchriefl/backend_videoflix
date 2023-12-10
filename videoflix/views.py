from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ResetPasswordSerializer, SetNewPasswordSerializer, GetThumbnailSerializer, GetPreviewVideoSerializer, GetVideoSerializer
from .models import CustomUser, Thumbnail, Video
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, logout
from django.urls import reverse
from urllib.parse import quote
from rest_framework.authtoken.models import Token
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page 
from django.conf import settings
from rest_framework.permissions import IsAuthenticated


CACHETTL = getattr(settings, 'CACHETTL', DEFAULT_TIMEOUT)

# @cachepage(CACHETTL)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_confirmation_email(request, user)
            return Response({'detail': 'User successfully created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_confirmation_email(self, request, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirmation_link = self.get_confirmation_link(request, uid, token)
        subject = 'Bestätigen Sie Ihre Registrierung'
        message = f'Vielen Dank für Ihre Registrierung. Bitte klicken Sie auf den folgenden Link, um Ihr Konto zu bestätigen: {confirmation_link}'
        from_email = 'noreply.videoflix@gmail.com'  # Hier Ihre E-Mail-Adresse oder eine allgemeine Adresse
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def get_confirmation_link(self, request, uid, token):
        return request.build_absolute_uri(reverse('confirm-registration', kwargs={'uid': uid, 'token': token}))
    
    
class ConfirmRegistrationView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode('utf-8')
            user = get_user_model().objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return redirect('http://localhost:4200/#/email_confirmed')
        else:
            return redirect('failure-page')
        
class LoginView(APIView):
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)            
            if user is not None:
                if user.email_confirmed == False:
                    return Response({'detail': 'Please confirm your email address first'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_name': user.user_name,
                        'email': user.email,
                        'id': user.id,
                        }, status=status.HTTP_200_OK)
                
            return Response({'detail': 'Email or password invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class RequestResetPasswordView(APIView):
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        email = request.data.get('email')
        user =  CustomUser.objects.filter(email=email).first()
        if user is not None:
            self.send_reset_password_email(request, user)
            return Response({'detail': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
     
    
    def send_reset_password_email(self, request, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = self.get_reset_link(request, uid, token)
        subject = 'Reset VideoFlix password'
        message = f'Hello {user.user_name}, Please click on the link to reset your password.: {reset_link}'
        from_email = 'noreply.videoflix@gmail.com'  # Hier Ihre E-Mail-Adresse oder eine allgemeine Adresse
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            return Response({'detail': 'Error sending email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_reset_link(self, request, uid, token):
        return request.build_absolute_uri(reverse('reset_pw', kwargs={'uid': uid, 'token': token}))
    
    
class ResetPasswordView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode('utf-8')
            user = get_user_model().objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            redirect_url = f'http://localhost:4200/#/set_new_password?user_id={uid}'
            return redirect(redirect_url)
        else:
            return redirect('failure-page')
            
class SetNewPasswordView(APIView):
    
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        new_password = request.data.get('password')
        user_id = request.data.get('user_id')
        user = CustomUser.objects.filter(id=user_id).first()      
        if user is not None:
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password has been changed succesfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class GetThumbnailsView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        thumbnails = Thumbnail.objects.all()
        serializer = GetThumbnailSerializer(thumbnails, many=True)  
        data = serializer.data
        for thumbnail in data:
            thumbnail['file_url'] = request.build_absolute_uri(thumbnail['thumbnail'])

        return Response(data)

        
class GetPreviewVideoView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        if video is None:
                return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            video_url = request.build_absolute_uri(video.file.url)
            serializer = GetPreviewVideoSerializer({'video_url': video_url})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class GetVideoView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request, video_id):
        video = get_object_or_404(Video, id=video_id)
        if video is None:
                return Response({'detail': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            video_url = request.build_absolute_uri(video.file.url)
            serializer = GetVideoSerializer({'video_url': video_url})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        
                        
                                
    
    
    
