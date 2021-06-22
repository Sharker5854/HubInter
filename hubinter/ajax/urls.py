from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
	path('tags_by_theme/', tags_by_theme, name='tags_by_theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)