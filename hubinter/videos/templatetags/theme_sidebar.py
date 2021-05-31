from django import template
from videos.models import Theme

register = template.Library()

@register.inclusion_tag('videos/inclusion_tags/_theme_sidebar.html')
def get_theme_sidebar():
	themes = Theme.objects.all()
	context = {
		'themes' : themes,
	}
	return context