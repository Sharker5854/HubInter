from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import FileExtensionValidator
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFit

import os
from delorean import Delorean
from .utils import *



class Theme(models.Model):
	name = models.CharField(verbose_name='Theme', max_length=100, unique=True)
	slug = models.SlugField(verbose_name='Slug', unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Theme'
		verbose_name_plural = 'Themes'
		ordering = ['name']





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




class Video(models.Model):
	title = models.CharField(verbose_name='Title', max_length=255, blank=False, null=False)
	slug = models.SlugField(verbose_name='Slug', max_length=300, unique=True)
	description = models.TextField(verbose_name='Description', max_length=2550)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, default=None,
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
		validators=[ FileExtensionValidator(allowed_extensions=['mp4', 'webm']), ],
		verbose_name='Video file'
	)
	views = models.PositiveIntegerField(verbose_name='Views', default=0)
	likes = models.PositiveIntegerField(verbose_name='Likes', default=0)
	dislikes = models.PositiveIntegerField(verbose_name='Dislikes', default=0)
	comments_amount = models.PositiveIntegerField(verbose_name='Comments', default=0)

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




class YoutubeVideo(models.Model):
	iframe_code = models.TextField(verbose_name="Video's HTML code", blank=False, null=False)
	title = models.CharField(verbose_name='Youtube Title', max_length=255, blank=False, null=False)
	slug = models.SlugField(verbose_name='Slug', max_length=300, unique=True)
	added_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, default=None,
		on_delete=models.CASCADE, verbose_name='Added by'
	)
	theme = models.ForeignKey('Theme', on_delete=models.PROTECT, verbose_name='Theme')
	tags = models.ManyToManyField('Tag', related_name='youtube_videos', verbose_name='Tags')
	added_at = models.DateTimeField(verbose_name='Added', auto_now_add=True)
	views = models.PositiveIntegerField(verbose_name='Views on Hubinter', default=0)
	preview = models.ImageField( # original preview
		upload_to='youtube_previews/%Y/%m/%d/',
		verbose_name='YouTube Preview', blank=True, 
		default=os.path.join(settings.BASE_DIR, 'media/default_pictures/default_preview.png')
	)
	cropped_preview = ImageSpecField( 
		processors=[ResizeToFit(width=270, height=212, upscale=True, mat_color='#26292E')], 
		source='preview', format='PNG'
	)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('youtube_video', kwargs={'slug' : self.slug})

	def get_added_at(self):
		delta = Delorean(datetime=self.added_at, timezone='Europe/Moscow')
		return delta.humanize().capitalize()




class Comment(models.Model):
	answer_for = models.ForeignKey('self', default=None, editable=False, verbose_name='Relative comment', on_delete=models.CASCADE)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL, editable=False,
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