from django.shortcuts import render, redirect
from django.contrib.auth.views import (
	LoginView, LogoutView, 
	PasswordChangeView, PasswordResetView, PasswordResetDoneView,
	PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.views.generic import CreateView, ListView
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy
from django.db.models import Prefetch

from .forms import (
	LoginForm, RegisterForm, 
	ChangePasswordForm, ResetPasswordForm, 
	ResetPasswordConfirmForm
)
from mixins import LoginRequired_WithMessage_Mixin
from videos.models import Video, YoutubeVideo
from .models import User
from itertools import chain
from logger import logger



class Login(LoginView):
	authentication_form = LoginForm
	template_name = 'accounts/login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.warning(request, 'You are already logged in as {}'.format(request.user.username))
			return redirect('profile', request.user.username)
		else:
			return super(Login, self).get(request, *args, **kwargs)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Authentication"

		if self.request.GET.get('next'):
			context['next'] = self.request.GET.get('next')
			self.request.session['next'] = context['next'] # add 'next' to the session, to use for redirection AFTER REGISTRATION

		return context

	def form_valid(self, form):
		messages.success(self.request, 'You authorized successfully!')
		super().form_valid(form)
		logger.info(f"User '{form.cleaned_data['username']}' logged in")
		return redirect(self.request.session.get('next', reverse('profile', kwargs={"username" : form.cleaned_data['username']})))

def save_social_authed_user(backend, user, response, *args, **kwargs):
	"""Correct user data before saving, if he authenticated through social network"""
	if backend.name == "google-oauth2":
		user.username = response.get("given_name", response["name"])
		user.name = response["name"]
		user.avatar = response["picture"]
		user.save()
		logger.info(f"User '{user.username}' logged in through google-oauth2")




class Register(CreateView):
	template_name = 'accounts/register.html'
	form_class = RegisterForm

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.warning(request, 'You are already logged in as {}'.format(request.user.username))
			return redirect('profile', request.user.username)
		else:
			return super().get(request, *args, **kwargs)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Registration"
		return context

	def form_valid(self, form):
		super().form_valid(form) # firstly, save new-user object
		logger.success(f"New user '{form.cleaned_data['username']}' registered successfully")
		messages.success(self.request, 'Congratulations! You registered successfully!')
		new_user = authenticate(
			username=form.cleaned_data['username'], 
			password=form.cleaned_data['password1']
		)
		login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')
		logger.info(f"New user '{form.cleaned_data['username']}' logged in after registering")
		return redirect(self.request.session.get('next', reverse('profile', kwargs={"username" : new_user.username})))




class Logout(LogoutView):

	@receiver(user_logged_out)
	def add_logout_msg(sender, request, **kwargs):
		"""Add logout message by signal, if user logged out"""
		if not request.user.is_anonymous:
			logger.info(f"User '{kwargs['user'].username}' logged out")
			messages.warning(request, "You have logged out of your account.")




class PasswordChange(LoginRequired_WithMessage_Mixin, PasswordChangeView):
	title = gettext_lazy('Password change')
	template_name = 'accounts/password_change.html'
	form_class = ChangePasswordForm

	def get_success_url(self):
		logger.success(f"User '{self.request.user.username}' changed password successfully")
		messages.success(self.request, "You changed password successfully!")
		return reverse('home')

	def form_valid(self, form):
		return super(PasswordChange, self).form_valid(form)




class PasswordReset(PasswordResetView):
	title = gettext_lazy('Password reset')
	template_name = 'accounts/password_reset.html'
	html_email_template_name = 'accounts/password_reset_email_template.html'
	form_class = ResetPasswordForm

	def form_valid(self, form):
		logger.info(f"An email to reset the password was sent to '{form.cleaned_data['email']}'")
		self.request.session["email_who_resets_password"] = form.cleaned_data["email"] # set cookie to get it in 'PasswordResetComplete' and write an user's email in logger ^_^
		return super().form_valid(form)


class PasswordResetDone(PasswordResetDoneView):
	title = gettext_lazy('Reset link was sent')
	template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
	title = gettext_lazy('Confirm password reset')
	template_name = 'accounts/password_reset_confirm.html'
	form_class = ResetPasswordConfirmForm
	sucess_url = reverse_lazy('password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
	title = gettext_lazy('Password reset completed')
	template_name = 'accounts/password_reset_complete.html'

	def get(self, request, *args, **kwargs):
		logger.success(f"User '{request.session.get('email_who_resets_password', '*email*')}' reset password successfully")
		del request.session["email_who_resets_password"]
		return super().get(request, *args, **kwargs)




class Profile(ListView):
	template_name = "accounts/profile.html"
	context_object_name = 'all_author_videos'
	paginate_by = 12

	def get_queryset(self):
		return sorted(
			list( chain(self.get_uploaded_videos(), self.get_youtube_videos()) ),
			key=self.get_datetime_sort_value,
			reverse=True
		)

	def get_uploaded_videos(self):
		return Video.objects.filter(
			author__username=self.kwargs["username"]
		).prefetch_related(
			Prefetch('tags')
		).select_related("theme", "author").order_by("-created_at")

	def get_youtube_videos(self):
		return YoutubeVideo.objects.filter(
			added_by__username=self.kwargs["username"]
		).prefetch_related(
			Prefetch('tags')
		).select_related("theme", "added_by").order_by("-added_at")

	def get_datetime_sort_value(self, video_obj):
		if isinstance(video_obj, Video):
			return video_obj.created_at
		else:
			return video_obj.added_at

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context["author_object"] = User.objects.filter(username=self.kwargs["username"]).first()
		if not context["author_object"]:
			raise Http404(f'User "{self.kwargs["username"]}" does not exist.')
		context["current_user"] = self.request.user
		return context