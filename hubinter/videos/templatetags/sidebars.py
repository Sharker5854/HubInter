from django import template
from videos.models import Theme, Tag

register = template.Library()


@register.inclusion_tag('videos/inclusion_tags/_theme_sidebar.html')
def get_theme_sidebar():
	themes = Theme.objects.all()
	context = {
		'themes' : themes,
	}
	return context



@register.inclusion_tag('videos/inclusion_tags/_tag_sidebar.html')
def get_tag_sidebar():
	tags = Tag.objects.all()
	context = {
		'tags' : tags,
	}
	return context