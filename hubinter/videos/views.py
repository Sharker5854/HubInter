from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.db.models import Q
from .models import *
from .utils import *
from delorean import Delorean
import loguru


# НАЧАЛ ДЕЛАТЬ САЙТ 10 МАЯ

'''
ЗАДАЧИ:

- АДМИНКА:
	Динамическое отображение нужных тэгов при выборе темы в админке (для Video)
	Доступ к редактированию видео админом

- ВИДЕО:
	Форма добавления видео
	Страница видео (DetailView)

- ВЗАИМОДЕЙСТВИЕ:
	Авторизация/Регистрация
	Пагинация (где надо)
'''


# ==================== CLASSES ==================== #

class Home(ListView):
	model = Video
	template_name = 'videos/index.html'
	context_object_name = 'videos'
	queryset = Video.objects.order_by('-created_at')




class SearchVideos(ListView):
	model = Video
	template_name = 'videos/video_search.html'
	context_object_name = 'found_videos'

	def get(self, request, *args, **kwargs):
		if request.GET.get('q').strip():
			queryset = self.get_queryset()
		else:
			return redirect('home')
		return super().get(request, *args, **kwargs)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.GET.get('q'):
			context['search_query'] = self.request.GET.get('q')
		return context

	def get_queryset(self):
		query = self.request.GET.get('q')
		queryset = self.model.objects.filter( 
			Q(title__icontains=query) | 
			Q(description__icontains=query) | 
			Q(tags__name__icontains=query) |
			Q(theme__name__icontains=query)
		)
		return queryset




class VideoDetail(DetailView):
	model = Video
	template_name = 'videos/video.html'
	context_object_name = 'video'

	def get_queryset(self):
		if self.kwargs['slug']:
			return Video.objects.filter(slug=self.kwargs['slug'])
		else:
			return Video.objects.first()



@method_decorator( cache_page(60 * 5), name="dispatch" )
class About(TemplateView):
	template_name = 'videos/about.html'


class Contact(FormView):
	template_name = 'videos/contact.html'
	form_class = About









# ==================== AJAX VIEWS ==================== #
'''
def get_videos_by_tag(request):
	videos_by_tag = [1, 2, 3]
	print(videos_by_tag)
	return JsonResponse({'videos_by_tag':videos_by_tag}, status=200)'''