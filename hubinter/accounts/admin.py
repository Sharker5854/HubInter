from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User
from urllib.parse import unquote


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('username', 'email', 'name', 'get_avatar')
		}),
		('Statistics', {
			'classes': ('collapse',),
			'fields': ('get_number_of_subscribers', 'registered_at'),
		}),
	)
	readonly_fields = ('username', 'email', 'name', 'get_avatar', 'get_number_of_subscribers', 'registered_at')
	search_fields = ('username', 'email')
	list_display = ('username', 'email', 'registered_at')
	ordering = ('-registered_at',)

	def get_avatar(self, obj):
		if obj.avatar:
			return mark_safe(f'<img src="{obj.get_avatar_url()}" width="120">')
		else:
			return '-'

	def get_number_of_subscribers(self, obj):
		return obj.subscribers.count()

	get_avatar.short_description = 'Avatar'
	get_number_of_subscribers.short_description = 'Subscribers'

	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, *args):
		return True