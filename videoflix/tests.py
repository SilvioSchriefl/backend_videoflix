from django.contrib.auth import get_user_model
from django.core import mail
from faker import Faker
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from .serializers import RegistrationSerializer

fake = Faker()


class RegisterViewTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')  
        data = {
            'user_name': 'testuser',
            'email': f'{fake.email()}-{fake.uuid4()}',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().user_name, 'testuser')
        

