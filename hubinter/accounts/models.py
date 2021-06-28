from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
	email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
	password = models.TextField(verbose_name='Password')
	name = models.CharField(max_length=100, verbose_name='Name')
	username = models.CharField(max_length=100, verbose_name='Username', unique=True)
	registered_at = models.DateTimeField(verbose_name='Registered', auto_now_add=True)
	avatar = models.ImageField(
		validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gmp']), ],
		upload_to='avatars/%Y/%m', verbose_name='Avatar', blank=True
	)
	subscribers = models.ManyToManyField(
		'self', related_name='subscriptions', 
		verbose_name='Subscribers'
	)
	notifications = models.ManyToManyField(
		'self', related_name='notified', 
		verbose_name='Notifications'
	)
	viewed_videos = models.ManyToManyField(
		'videos.Video', related_name='viewed_by', 
		verbose_name='Viewed videos'
	)
	liked_videos = models.ManyToManyField(
		'videos.Video', related_name='liked_by', 
		verbose_name='Liked videos'
	)
	disliked_videos = models.ManyToManyField(
		'videos.Video', related_name='disliked_by', 
		verbose_name='Disliked videos'
	)

	def __str__(self):
		return self.username