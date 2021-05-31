from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import *
from delorean import Delorean
import loguru

# НАЧАЛ ДЕЛАТЬ САЙТ 10 МАЯ

'''
ЗАДАЧИ:

АДМИНКА:
Динамическое отображение нужных тэгов при выборе темы в админке (для Video)
Доступ к редактированию видео админом

ВИДЕО:
Приведение превьюшки к нужному разрешению и рекомендованные размеры (исходные 270 на 211)
'''


# ==================== CLASSES ==================== #

class Home(ListView):
	model = Video
	template_name = 'videos/index.html'
	queryset = Video.objects.order_by('-created_at')
	context_object_name = 'videos'

	# def get_queryset(self, request):
	# 	pass


class VideoDetail(DetailView):
	model = Video
	template_name = 'videos/video.html'
	context_object_name = 'video'

	def get_queryset(self):
		if self.kwargs['slug']:
			return Video.objects.filter(slug=self.kwargs['slug'])
		else:
			return Video.objects.first()



class About(TemplateView):
	template_name = 'videos/about.html'
		

class Contact(FormView):
	template_name = 'videos/contact.html'
	form_class = About