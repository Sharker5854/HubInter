from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
	Home, VideoDetail, SearchVideos, 
	AddVideo, About, Contact
)


urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('video/<slug:slug>/', VideoDetail.as_view(), name='video'),
	path('search/', SearchVideos.as_view(), name='search'),

	path('add_video/', AddVideo.as_view(), name='add_video'),

	path('about/', About.as_view(), name='about'),
	path('contact/', Contact.as_view(), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)