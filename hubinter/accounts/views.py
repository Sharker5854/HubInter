from django.shortcuts import render, redirect
from django.contrib.auth.views import (
	LoginView, LogoutView, 
	PasswordChangeView, PasswordResetView, PasswordResetDoneView,
	PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy

from .forms import (
	LoginForm, RegisterForm, 
	ChangePasswordForm, ResetPasswordForm, 
	ResetPasswordConfirmForm
)
from mixins import LoginRequired_WithMessage_Mixin
from .models import User



class Login(LoginView):
	authentication_form = LoginForm
	template_name = 'accounts/login.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.warning(request, 'You are already logged in as {}'.format(request.user.username))
			return redirect('home')
		else:
			return super(Login, self).get(request, *args, **kwargs)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Authentication"

		if not self.request.GET.get('next'):
			context['next'] = reverse('home')
		else:
			context['next'] = self.request.GET.get('next')
			self.request.session['next'] = context['next'] # add 'next' to the session, to use for redirection AFTER REGISTRATION

		return context

	def form_valid(self, form):
		messages.success(self.request, 'You authorized successfully!')
		return super(Login, self).form_valid(form)

def save_social_authed_user(backend, user, response, *args, **kwargs):
	"""Correct user data before saving, if he authenticated through social network"""
	if backend.name == "google-oauth2":
		user.username = response.get("given_name", response["name"])
		user.name = response["name"]
		user.avatar = response["picture"]
		user.save()




class Register(CreateView):
	template_name = 'accounts/register.html'
	form_class = RegisterForm

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			messages.warning(request, 'You are already logged in as {}'.format(request.user.username))
			return redirect('home')
		else:
			return super(Register, self).get(request, *args, **kwargs)

	def get_success_url(self):
		return self.request.session.get('next', reverse('home'))

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Registration"
		return context

	def form_valid(self, form):
		super(Register, self).form_valid(form) # firstly, save new-user object
		messages.success(self.request, 'Congratulations! You registered successfully!')
		new_user = authenticate(
			username=form.cleaned_data['username'], 
			password=form.cleaned_data['password1']
		)
		login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')
		return HttpResponseRedirect(self.get_success_url())




class Logout(LogoutView):

	@receiver(user_logged_out)
	def add_logout_msg(sender, request, **kwargs):
		"""Add logout message by signal, if user is was authenticated"""
		if not request.user.is_anonymous:
			messages.warning(request, "You have logged out of your account.")




class PasswordChange(LoginRequired_WithMessage_Mixin, PasswordChangeView):
	title = gettext_lazy('Password change')
	template_name = 'accounts/password_change.html'
	form_class = ChangePasswordForm

	def get_success_url(self):
		messages.success(self.request, "You changed password successfully!")
		return reverse('home')

	def form_valid(self, form):
		return super(PasswordChange, self).form_valid(form)




class PasswordReset(PasswordResetView):
	title = gettext_lazy('Password reset')
	template_name = 'accounts/password_reset.html'
	html_email_template_name = 'accounts/password_reset_email_template.html'
	form_class = ResetPasswordForm


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