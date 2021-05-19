from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import *
from delorean import Delorean
import loguru


'''
ЗАДАЧИ:
Изучить классы из generic
'''



# ==================== CLASSES ==================== #

class Home(ListView):
	model = Video
	template_name = 'videos/index.html'





# ==================== FUNCTIONS ==================== #

class About(TemplateView):
	template_name = 'videos/about.html'
		

class Contact(FormView):
	template_name = 'videos/contact.html'
	form_class = About
