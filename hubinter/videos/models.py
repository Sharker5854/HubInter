import os
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models import signals
from django.utils.text import slugify
from delorean import Delorean
from .utils import *
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit


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
		'Video', related_name='viewed_by', 
		verbose_name='Viewed videos'
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

	class Meta:
		verbose_name = 'Theme'
		verbose_name_plural = 'Themes'
		ordering = ['name']

@receiver(signals.pre_save, sender=Theme)
def populate_slug(sender, instance, **kwargs):
	'''Due to the fact that the slug doesn't change while editing the name in admin panel,
	should use presave signal to change slug again'''
	instance.slug = slugify(instance.name)





class Tag(models.Model):
	name = models.CharField(verbose_name='Tag', max_length=50, unique=True)
	slug = models.SlugField(verbose_name='Slug', unique=True)
	theme = models.ForeignKey('Theme', on_delete=models.CASCADE, verbose_name='Theme')
	created_at = models.DateTimeField(verbose_name='Tag added', auto_now_add=True)

	def __str__(self):
		return self.name

	def get_created_at(self):
		delta = Delorean(datetime=self.created_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()

	class Meta:
		verbose_name = 'Tag'
		verbose_name_plural = 'Tags'
		ordering = ['theme']

@receiver(signals.pre_save, sender=Tag)
def populate_slug(sender, instance, **kwargs):
	'''Due to the fact that the slug doesn't change while editing the name in admin panel,
	should use presave signal to change slug again'''
	instance.slug = slugify(instance.name)





class Video(models.Model):
	title = models.CharField(verbose_name='Title', max_length=255, blank=False, null=False)
	slug = models.SlugField(verbose_name='Slug', max_length=300, unique=True)
	description = models.TextField(verbose_name='Description', max_length=2550)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,default=None,
		on_delete=models.CASCADE, verbose_name='Author'
	)
	theme = models.ForeignKey('Theme', on_delete=models.PROTECT, verbose_name='Theme')
	tags = models.ManyToManyField('Tag', related_name='videos', verbose_name='Tags')
	created_at = models.DateTimeField(verbose_name='Published', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Updated', auto_now=True)
	preview = models.ImageField( # original preview
		upload_to='previews/%Y/%m/%d/', 
		validators=[ FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'svg', 'gmp']), ],
		verbose_name='Preview file', blank=True, default=os.path.join(settings.BASE_DIR, 'media/default_pictures/default_preview.png')
	)
	cropped_preview = ImageSpecField( 
		processors=[ResizeToFit(width=270, height=212, upscale=True, mat_color='#26292E')], 
		source='preview', format='PNG'
	)
	video = models.FileField(
		upload_to='videos/%Y/%m/%d/', 
		validators=[ FileExtensionValidator(allowed_extensions=['mov', 'mp4', 'mpeg4', 'avi', 'mpegps', 'flv']), ],
		verbose_name='Video file'
	)
	is_published = models.BooleanField(default=True, verbose_name='Is Published')
	views = models.IntegerField(verbose_name='Views', default=0)
	likes = models.IntegerField(verbose_name='Likes', default=0)
	dislikes = models.IntegerField(verbose_name='Dislikes', default=0)
	comments_amount = models.IntegerField(verbose_name='Comments', default=0)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('video', kwargs={'slug' : self.slug})

	def get_created_at(self):
		delta = Delorean(datetime=self.created_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()

	def get_updated_at(self):
		delta = Delorean(datetime=self.updated_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()

	class Meta:
		verbose_name = 'Video'
		verbose_name_plural = 'Videos'
		ordering = ['-created_at']

# @receiver(signals.pre_save, sender=Video)
# def populate_slug(sender, instance, **kwargs):
# 	''' Due to the fact that the slug doesn't change while editing the name in admin panel,
# 	should use presave signal to change slug again'''
# 	instance.slug = slugify(instance.title)





'''
class YoutubeVideo(models.Model):
	youtube_link = models.TextField(verbose_name='Youtube link')

	def is_yotube_link(self, link):
		pass
'''





class Comment(models.Model):
	answer_for = models.ForeignKey('self', default=None, editable=False, verbose_name='Relative comment', on_delete=models.CASCADE)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, editable=False, 
		#default=None, null=True, blank=True,
		verbose_name='Author', on_delete=models.CASCADE
	)
	text = models.TextField(verbose_name='Text', max_length=1000)
	video = models.ForeignKey('Video', on_delete=models.CASCADE, editable=False, verbose_name='Video')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Added')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

	def __str__(self):
		return self.title

	def get_created_at(self):
		delta = Delorean(datetime=self.created_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()

	def get_updated_at(self):
		delta = Delorean(datetime=self.updated_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()

	class Meta:
		verbose_name = 'Comment'
		verbose_name_plural = 'Comments'
		ordering = ['-created_at']