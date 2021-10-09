from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
	Home, VideoDetail, YoutubeVideoDetail, SearchVideos, 
	AddVideo, AddYoutubeVideo, DeleteVideo, DeleteYoutubeVideo, About, Contact
)


urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('video/<slug:slug>/', VideoDetail.as_view(), name='video'),
	path('youtube_video/<slug:slug>/', YoutubeVideoDetail.as_view(), name='youtube_video'),
	path('search/', SearchVideos.as_view(), name='search'),

	path('add_video/', AddVideo.as_view(), name='add_video'),
	path('add_youtube_video/', AddYoutubeVideo.as_view(), name='add_youtube_video'),

	path('delete_video/<slug:slug>/', DeleteVideo.as_view(), name='delete_video'),
	path('delete_youtube_video/<slug:slug>/', DeleteYoutubeVideo.as_view(), name='delete_youtube_video'),

	path('about/', About.as_view(), name='about'),
	path('contact/', Contact.as_view(), name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)