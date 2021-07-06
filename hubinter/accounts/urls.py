from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
	Login, Register, Logout, 
	PasswordChange, PasswordReset, PasswordResetDone,
	PasswordResetConfirm, PasswordResetComplete
)


urlpatterns = [
	path('login/', Login.as_view(), name='login'),
	path('register/', Register.as_view(), name='register'),
	path('logout/', Logout.as_view(), name='logout'),

	path('password_change/', PasswordChange.as_view(), name='password_change'),
	path('password_reset/', PasswordReset.as_view(), name='password_reset'),
	path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
	path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)