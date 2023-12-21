
from django.contrib import admin
from django.urls import path, include
from videoflix.views import RegisterView, ConfirmRegistrationView, LoginView, ResetPasswordView, RequestResetPasswordView, SetNewPasswordView, GetThumbnailsView, GetPreviewVideoView, GetVideoView, WatchlistView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-registration/<str:uid>/<str:token>/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
    path('request_reset_password/', RequestResetPasswordView.as_view(), name='request_reset_pw'),
    path('reset_pw/<str:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset_pw'),
    path('set_password/', SetNewPasswordView.as_view(), name='set_password'),
    path('log_in/', LoginView.as_view(), name='login'),
    path('thumbnail/', GetThumbnailsView.as_view(), name='thumbnail'),
    path('video_preview/<int:video_id>/', GetPreviewVideoView.as_view(), name='preview_video'),
    path('video/<int:video_id>/', GetVideoView.as_view(), name='video'),
    path('watchlist/', WatchlistView.as_view(), name='watchlist'),
    path('watchlist/<int:user_id>/', WatchlistView.as_view(), name='get_watchlist'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('django-rq/', include('django_rq.urls')),
] + staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
