
from django.contrib import admin
from django.urls import path
from videoflix.views import RegisterView, ConfirmRegistrationView, LoginView, ResetPasswordView, RequestResetPasswordView, SetNewPasswordView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-registration/<str:uid>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
    path('request_reset_password/', RequestResetPasswordView.as_view(), name='request_reset_pw'),
    path('reset_pw/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_pw'),
    path('set_password/', SetNewPasswordView.as_view(), name='set_password'),
    path('log_in/', LoginView.as_view(), name='login'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
