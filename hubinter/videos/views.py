from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import IntegrityError
from django.views.generic import ListView, DetailView, TemplateView, FormView, CreateView
from django.db.models import Q
from django.db.models import Prefetch
from django.core import files
from django.contrib import messages

from .models import *
from .utils import *
from .forms import AddVideoForm, AddYoutubeVideoForm
from mixins import LoginRequired_WithMessage_Mixin
from delorean import Delorean
import iuliia
import loguru
import uuid


# НАЧАЛ ДЕЛАТЬ САЙТ 10 МАЯ

'''
ЗАДАЧИ:

- АДМИНКА:
	Динамическое отображение нужных тэгов при выборе темы в админке (для Video)
	Доступ к редактированию видео админом

- ВИДЕО:
	Страница видео (DetailView)

- ВЗАИМОДЕЙСТВИЕ:
	Настройка YouTube видео в админке, довести маршрутизацию до ума, доделать установку дефолтной превьюшки
	Видеопроигрыватель
	Комменты, лайки, подписки, уведомления, "Поделиться"
	Профиль
	Алгоритм рекомендаций...
	Отправка почты (Contact), About
	Пагинация (где надо)
	Кэширование, логирование
	*ДЕПЛОЙ* (после него, настроить авторизацию через соц. сети, https-протокол, бд на AWS)



- ДОДЕЛАТЬ:
	Проверка CSRF при ajax-запросах
	Не забыть про автозаполнение слага при редактировании объекта
	Анимацию фильтрации по тэгам на главной
	Стили для формы добавления видео
'''


# ==================== CLASSES ==================== #

class Home(ListView):
	model = Video
	template_name = 'videos/index.html'
	context_object_name = 'videos'
	queryset = Video.objects.prefetch_related(
		Prefetch('tags')
	).select_related('theme', 'author').filter(is_published=True).order_by('-created_at')




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
		queryset = self.model.objects.prefetch_related(
			Prefetch('tags')
		).select_related('theme', 'author').filter(
			Q(title__icontains=query) | 
			Q(description__icontains=query) | 
			Q(tags__name__icontains=query) |
			Q(theme__name__icontains=query),
			is_published=True
		)
		return queryset




class VideoDetail(DetailView):
	model = Video
	template_name = 'videos/video_detail.html'
	context_object_name = 'video'

	def get_queryset(self):
		if self.kwargs['slug']:
			return Video.objects.filter(slug=self.kwargs['slug'])
		else:
			return Video.objects.first()




class YoutubeVideoDetail(DetailView):
	model = YoutubeVideo
	template_name = 'videos/video_detail.html'
	context_object_name = 'video'

	def get_queryset(self):
		if self.kwargs['slug']:
			return YoutubeVideo.objects.filter(slug=self.kwargs['slug'])
		else:
			return YoutubeVideo.objects.first()




class AddVideo(LoginRequired_WithMessage_Mixin, CreateView):
	model = Video
	form_class = AddVideoForm
	template_name = "videos/add_video.html"

	def form_valid(self, form):
		self.object = form.save(commit=False)

		self.object.author = self.request.user
		self.object.slug = slugify( iuliia.translate(self.object.title, iuliia.TELEGRAM) )
		# if title on Russian, will transliterate slug. Else - leave without changes

		try:
			self.object.save()
		except IntegrityError: #add 5 random symbols to slug, if it is not unique
			self.object.slug = slugify( 
				iuliia.translate(self.object.title, iuliia.TELEGRAM)
			) + "_" + str(uuid.uuid4())[:5]
			self.object.save() #and try to save again

		form.save_m2m() #unecessary, to save selected tags
		messages.success(self.request, 'Video uploaded successfully!')
		return HttpResponseRedirect(self.get_success_url())


	def form_invalid(self, form):
		messages.error(self.request, 'Please fill in all the fields correctly!')
		return super(AddVideo, self).form_invalid(form)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_form_type'] = 'upload'
		return context




class AddYoutubeVideo(LoginRequired_WithMessage_Mixin, CreateView):
	model = YoutubeVideo
	form_class = AddYoutubeVideoForm
	template_name = "videos/add_video.html"

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_form_type'] = 'youtube'
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		parser = form.cleaned_data['parser']

		self.object.iframe_code = parser.iframe
		self.object.title = parser.get_title()			
		self.object.slug = slugify( iuliia.translate(self.object.title, iuliia.TELEGRAM) )
		self.object.added_by = self.request.user
		self.object.preview = files.File( parser.get_preview_file(), name=str(uuid.uuid4())[10:]+".png" )
		
		try:
			self.object.save()
		except IntegrityError:
			self.object.slug = slugify( 
				iuliia.translate(self.object.title, iuliia.TELEGRAM) 
			) + "_" + str(uuid.uuid4())[:5]
			self.object.save()

		form.save_m2m()
		messages.success(self.request, 'Your YouTube video added successfully!')
		return HttpResponseRedirect(self.get_success_url())


	def form_invalid(self, form):
		messages.error(self.request, 'Please fill in all the fields correctly!')
		return super(AddYoutubeVideo, self).form_invalid(form)





@method_decorator( cache_page(60 * 5), name="dispatch" )
class About(TemplateView):
	template_name = 'about.html'


class Contact(FormView):
	template_name = 'contact.html'
	form_class = About # 