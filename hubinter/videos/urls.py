from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('video/<slug:slug>/', VideoDetail.as_view(), name='video'),
	path('about/', About.as_view(), name='about'),
	path('contact/', Contact.as_view(), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)