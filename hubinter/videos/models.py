from django.db import models
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from delorean import Delorean


class User(AbstractUser):
	email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
	password = models.TextField(verbose_name='Password')
	name = models.CharField(max_length=100, verbose_name='Name')
	username = models.CharField(max_length=100, verbose_name='Username', unique=True)
	registered_at = models.DateTimeField(verbose_name='Registered', auto_now_add=True)
	avatar = models.ImageField(
		validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg']), ],
		upload_to='avatars/%Y/%m', verbose_name='Avatar', blank=True
	)
	subscribers = models.ManyToManyField(
		'self', related_name='subscriptions', 
		verbose_name='Subscribers'
	)
	notifications = models.ManyToManyField(
		'self', related_name='notified', 
		verbose_name='Notificatiosn'
	)
	liked_videos = models.ManyToManyField(
		'Video', related_name='liked_by', 
		verbose_name='Liked videos'
	)
	disliked_videos = models.ManyToManyField(
		'Video', related_name='disliked_by', 
		verbose_name='Disliked videos'
	)

	def __str__(self):
		return self.username



class Theme(models.Model):
	name = models.CharField(verbose_name='Theme', max_length=100, unique=True)
	slug = models.SlugField(verbose_name='Slug', unique=True)

	def __str__(self):
		return self.name



class Tag(models.Model):
	name = models.CharField(verbose_name='Tag', max_length=50, unique=True)
	slug = models.SlugField(verbose_name='Slug', unique=True)
	theme = models.ForeignKey('Theme', on_delete=models.CASCADE, verbose_name='Relative theme')
	created_at = models.DateTimeField(verbose_name='Tag added', auto_now_add=True)

	def __str__(self):
		return self.name



class Video(models.Model):
	title = models.CharField(verbose_name='Video', max_length=255)
	slug = models.SlugField(verbose_name='Slug', unique=True)
	description = models.TextField(verbose_name='Description')
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
	created_at = models.DateTimeField(verbose_name='Video added', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Video updated', auto_now=True)
	preview = models.ImageField(
		upload_to='previews/%Y/%m/%d/', 
		validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg']), ],
		verbose_name='Preview file', blank=True
	)
	video = models.FileField(
		upload_to='videos/%Y/%m/%d/', 
		validators=[ FileExtensionValidator(allowed_extensions=['mov', 'mp4', 'mpeg4', 'avi', 'mpegps', 'flv']), ],
		verbose_name='Video file'
	)
	views = models.IntegerField(verbose_name='Views', default=0)
	likes = models.IntegerField(verbose_name='Likes', default=0)
	dislikes = models.IntegerField(verbose_name='Dislikes', default=0)
	comments_amount = models.IntegerField(verbose_name='Comments amount', default=0)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('video', kwargs={'slug' : self.slug})


'''
class YoutubeVideo(models.Model):
	youtube_link = models.TextField(verbose_name='Youtube link')

	def is_yotube_link(self, link):
		pass
'''



class Comment(models.Model):
	answer_for = models.ForeignKey('self', default='', verbose_name='Relative comment', on_delete=models.CASCADE)
	author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
	text = models.TextField(verbose_name='Text', max_length=1000)
	video = models.ForeignKey('Video', on_delete=models.CASCADE, verbose_name='Video')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Comment added')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Comment updated')

	def __str__(self):
		return self.title