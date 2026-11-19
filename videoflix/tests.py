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
        



from unittest.mock import patch
from rest_framework.authtoken.models import Token
from .models import Video


@patch('videoflix.signals.create_thumbnail')
class OwnershipTests(APITestCase):
    """Eingeloggte Nutzer dürfen nur ihre eigenen Videos und ihre eigene Watchlist sehen und ändern."""

    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(email='alice@example.com', password='pw', user_name='alice')
        self.bob = User.objects.create_user(email='bob@example.com', password='pw', user_name='bob')
        self.bob.watchlist = [1, 2]
        self.bob.save()

    def login_as(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def video_of(self, user):
        return Video.objects.create(title='Urlaub', user=user)

    def test_owner_can_delete_own_video(self, _thumb):
        video = self.video_of(self.alice)
        self.login_as(self.alice)
        response = self.client.delete(reverse('delete_video', args=[video.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Video.objects.filter(id=video.id).exists())

    def test_cannot_delete_video_of_other_user(self, _thumb):
        video = self.video_of(self.bob)
        self.login_as(self.alice)
        response = self.client.delete(reverse('delete_video', args=[video.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Video.objects.filter(id=video.id).exists())

    def test_cannot_edit_video_of_other_user(self, _thumb):
        video = self.video_of(self.bob)
        self.login_as(self.alice)
        response = self.client.patch(reverse('video'), {'id': video.id, 'title': 'gehackt'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        video.refresh_from_db()
        self.assertEqual(video.title, 'Urlaub')

    def test_cannot_read_watchlist_of_other_user(self, _thumb):
        self.login_as(self.alice)
        response = self.client.get(reverse('get_watchlist', args=[self.bob.id]))
        self.assertNotEqual(response.data.get('watchlist'), [1, 2])

    def test_cannot_change_watchlist_of_other_user(self, _thumb):
        self.login_as(self.alice)
        self.client.patch(reverse('get_watchlist', args=[self.bob.id]), {'watchlist': []}, format='json')
        self.bob.refresh_from_db()
        self.assertEqual(self.bob.watchlist, [1, 2])

    def test_watchlist_returns_own_list(self, _thumb):
        self.alice.watchlist = [7]
        self.alice.save()
        self.login_as(self.alice)
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.data['watchlist'], [7])
