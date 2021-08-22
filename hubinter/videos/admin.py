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
			'fields': ('title', 'slug', 'author', 'description', 'theme', 'tags', 'get_preview')
		}),
		('Statistics', {
			'classes': ('collapse',),
			'fields': ('views', 'likes', 'dislikes', 'comments_amount', 
				'created_at', 'updated_at'),
		}),
	)
	readonly_fields = (
		'views', 'likes', 'dislikes', 'comments_amount', 
		'created_at', 'updated_at'
	)
	prepopulated_fields = {'slug' : ('title',)}
	search_fields = ('title', 'author')
	list_filter = ('theme', 'tags', 'created_at')
	list_display = (
		'title', 'author', 'theme',  
		'created_at', 'get_preview_list_display',
	)
	ordering = ('-created_at',)

	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False
	'''
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
			return mark_safe(f'<img src="{unquote(obj.preview.url)}" width="200">')
		else:
			return '-'

	def humanize_created_at(self, obj):
		return obj.get_created_at()

	def humanize_updated_at(self, obj):
		return obj.get_updated_at()

	get_preview_list_display.short_description = 'Preview'
	get_preview.short_description = 'Preview'
	humanize_created_at.short_description = 'Published'
	humanize_updated_at.short_description = 'Updated'




@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('title', 'slug', 'added_by', 'theme', 'tags', 'get_preview')
		}),
		('Statistics', {
			'classes': ('collapse',),
			'fields': ('views', 'added_at'),
		}),
	)
	readonly_fields = (
		'title', 'slug', 'theme', 'tags', 'preview',
		'views', 'added_at'
	)
	search_fields = ('title', 'added_by')
	list_filter = ('theme', 'tags', 'added_at')
	list_display = (
		'title', 'added_by', 'theme',  
		'humanize_added_at', 'get_preview_list_display',
	)
	ordering = ('-added_at',)

	def has_add_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def get_preview_list_display(self, obj):
		if obj.preview:
			return mark_safe(f'<img src="{unquote(obj.cropped_preview.url)}" width="100">')
		else:
			return '-'

	def get_preview(self, obj):
		if obj.preview:
			return mark_safe(f'<img src="{unquote(obj.preview.url)}" width="200">')
		else:
			return '-'

	def humanize_added_at(self, obj):
		return obj.get_added_at()

	get_preview_list_display.short_description = 'Preview'
	get_preview.short_description = 'Preview'
	humanize_added_at.short_description = 'Published'




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	fields = ('author', 'text', 'video', 'created_at')
	readonly_fields = ('author', 'text', 'video', 'created_at')
	search_fields = ('author', 'text')
	list_filter = ('created_at',)
	list_display = ('author', 'video', 'humanize_created_at')
	ordering = ('-created_at',)

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def humanize_created_at(self, obj):
		return obj.get_created_at()

	humanize_created_at.short_description = 'Written'
