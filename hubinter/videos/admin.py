from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from delorean import Delorean
from .models import *
from urllib.parse import unquote


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
	fields = ('name', 'slug')
	prepopulated_fields = {'slug' : ('name',)}
	search_fields = ('name',)
	ordering = ('name',)
	list_display = ('name',)



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	fields = ('name', 'slug', 'theme')
	prepopulated_fields = {'slug' : ('name',)}
	search_fields = ('name',)
	ordering = ('-created_at',)
	list_filter = ('theme',)
	list_display = ('name', 'theme', 'humanize_created_at')

	def humanize_created_at(self, obj):
		return obj.get_created_at()

	humanize_created_at.short_description = 'Tag added'



@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'description', 'theme', 'tags', 'preview', 'video',)
		}),
		('Statistics', {
			'classes': ('collapse',),
			'fields': ('is_published', 'views', 'likes', 'dislikes', 'comments_amount', 
				'humanize_created_at', 'humanize_updated_at'),
		}),
	)
	readonly_fields = (
		'views', 'likes', 'dislikes', 'comments_amount', 
		'humanize_created_at', 'humanize_updated_at', 'is_published'
	)
	prepopulated_fields = {'slug' : ('title',)}
	search_fields = ('title', 'author')
	list_filter = ('theme', 'tags', 'created_at', 'is_published')
	list_display = (
		'title', 'theme', 'views', 
		'humanize_created_at', 'get_preview_list_display', 'is_published',
	)
	ordering = ('-created_at',)
	'''
	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
	'''

	def save_model(self, request, obj, form, change):
		"""Redefining the method of saving model to add author and right to edit video"""
		if not change: # if record is CREATING
			obj.author = request.user

		super(VideoAdmin, self).save_model(
			request=request,
			obj=obj,
			form=form,
			change=change
		)

	def get_preview_list_display(self, obj):
		if obj.preview:
			return mark_safe(f'<img src="{unquote(obj.cropped_preview.url)}" width="100">')
		else:
			return '-'

	def get_preview(self, obj):
		if obj.preview:
			return mark_safe(f'<img src="{unquote(obj.preview.url)}" width="120">')
		else:
			return '-'

	def get_video(self, obj):
		return mark_safe(f'''
			<video controls="controls" width="200">
				<source src="{unquote(obj.video.url)}">
			</video>
		''')

	def humanize_created_at(self, obj):
		return obj.get_created_at()

	def humanize_updated_at(self, obj):
		return obj.get_updated_at()

	get_preview_list_display.short_description = 'Preview'
	get_preview.short_description = 'Preview'
	get_video.short_description = 'Video'
	humanize_created_at.short_description = 'Published'
	humanize_updated_at.short_description = 'Updated'




@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
	pass



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	fields = ('author', 'text', 'answer_for', 'video', 'created_at', 'updated_at')
	readonly_fields = ('author', 'text', 'answer_for', 'video', 'created_at', 'updated_at')
	search_fields = ('author', 'text')
	list_filter = ('created_at',)
	list_display = ('author', 'video', 'answer_for', 'humanize_created_at')
	ordering = ('-created_at',)

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def humanize_created_at(self, obj):
		return obj.get_created_at()

	def humanize_updated_at(self, obj):
		return obj.get_updated_at()

	humanize_created_at.short_description = 'Written'
	humanize_updated_at.short_description = 'Updated'
