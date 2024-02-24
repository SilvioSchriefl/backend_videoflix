from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, LoginSerializer, ResetPasswordSerializer, SetNewPasswordSerializer, VideoSerializer, WatchlistSerializer
from .models import CustomUser, Video
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


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)




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
        subject = 'Confirm your registration'
        message = f'Hello {user.user_name}. Thank you for your registration. Please click the following link to verify your account {confirmation_link}'
        from_email = 'noreply@videoflix.com'  
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
            return redirect('https://videoflix.silvio-schriefl.de/#/user_not_found')
        if user.email_confirmed:
            return redirect('https://videoflix.silvio-schriefl.de/#/token_used')
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return redirect('https://videoflix.silvio-schriefl.de/#/email_confirmed')
        else:
            return redirect('https://videoflix.silvio-schriefl.de/#/email_not_confirmed')
        
class LoginView(APIView):
    
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)            
            if user is not None:
                if user.email_confirmed == False:
                    return Response({'detail': 'Please confirm your email address first'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    token, created = Token.objects.get_or_create(user=user)
                    if not created:
                        token.delete()
                        token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'user_name': user.user_name,
                        'email': user.email,
                        'id': user.id,
                        'watchlist': user.watchlist
                        }, status=status.HTTP_200_OK)
                
            return Response({'detail': 'Email or password invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated] 
   
    def post(self, request):
        logout(request)
        return Response({"detail": "Logout erfolgreich."}, status=status.HTTP_200_OK)
        
        
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
        from_email = 'noreply@videoflix' 
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            return Response({'detail': 'Error sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
            redirect_url = f'https://videoflix.silvio-schriefl.de/#/set_new_password?user_id={uid}'
            return redirect(redirect_url)
        else:
            return redirect('https://videoflix.silvio-schriefl.de/#/set_new_password_error')
            
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
        

        

        
class WatchlistView(APIView):
    
    permission_classes = [IsAuthenticated] 
   
    
    def patch(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = WatchlistSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = WatchlistSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated] 
    

    def delete(self, request):
        user = request.user  
        
        if user is not None:
            user.delete()
            return Response({"detail": "Account successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
class VideoView(APIView):

    permission_classes = [IsAuthenticated]
  

    def post(self, request):
        user = request.user
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get (self, request):
        user = request.user
        if user:
            videos = Video.objects.filter(user=user)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
        
 
        

        
    
        
                        
                                
    
    
    
