from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver

class LoginRequired_WithMessage_Mixin(LoginRequiredMixin):
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_anonymous:
			messages.error(request, "To access this page, you need to log in!")
		return super(LoginRequired_WithMessage_Mixin, self).dispatch(request, *args, **kwargs)