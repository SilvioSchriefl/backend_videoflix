
from django.contrib import admin
from django.urls import path
from videoflix.views import RegisterView, ConfirmRegistrationView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-registration/<str:uid>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
]
