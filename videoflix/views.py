from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from .models import CustomUser
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import quote




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
    
    
    
