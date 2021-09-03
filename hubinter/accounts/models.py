from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

import os
from urllib.parse import unquote


class User(AbstractUser):
	USERNAME_FIELD = 'username' #provide ability for django's backend to determine a username field for AUTHENTICATION

	email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
	password = models.TextField(verbose_name='Password')
	name = models.CharField(max_length=100, verbose_name='Name')
	username = models.CharField(max_length=100, verbose_name='Username', unique=True)
	registered_at = models.DateTimeField(verbose_name='Registered', auto_now_add=True)
	avatar = models.ImageField(
		validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gmp']), ],
		upload_to='avatars/%Y/%m', verbose_name='Avatar', blank=True, 
		default=os.path.join(settings.BASE_DIR, 'media/default_pictures/default_avatar.jpg')
	)
	subscribers = models.ManyToManyField(
		'self', related_name='subscriptions', 
		verbose_name='Subscribers'
	)
	notifications = models.ManyToManyField( # people, who notified about new videos of THIS USER
		'self', related_name='notified', 
		verbose_name='Notifications'
	)
	viewed_videos = models.ManyToManyField(
		'videos.Video', related_name='viewed_by', 
		verbose_name='Viewed videos'
	)
	viewed_yt_videos = models.ManyToManyField(
		'videos.YoutubeVideo', related_name='yt_viewed_by', 
		verbose_name='Viewed YouTube videos'
	)
	liked_videos = models.ManyToManyField(
		'videos.Video', related_name='liked_by', 
		verbose_name='Liked videos'
	)
	disliked_videos = models.ManyToManyField(
		'videos.Video', related_name='disliked_by', 
		verbose_name='Disliked videos'
	)
	
	def get_avatar_url(self):
		""" If avatar.url is external link, return it without prefix '/media/' """
		url = unquote(self.avatar.url)
		if "https:/" in url or "http:/" in url:
			return url.replace("/media/", "")
		return url

	def get_absolute_url(self):
		return "#"

	def __str__(self):
		return self.username