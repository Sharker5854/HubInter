from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.contrib import messages

from logger import logger
from functools import wraps



class ErrorTrackerView(View):
	"""Catch all exceptions in project's class-based views and log them."""

	def dispatch(self, request, *args, **kwargs):
		try:
			response = super().dispatch(request, *args, **kwargs)
		except Exception as error:
			logger.error(f"An error {repr(error)} occurred in generic view when accessing the page '{request.method} {request.get_full_path()}'")
			return HttpResponseBadRequest()
		else:
			return response



def error_tracker_view(func_view):
	"""Decorator that catch all exceptions in project's function-based views and log them."""

	@wraps(func_view)
	def wrapper(request, *args, **kwargs):
		try:
			with transaction.atomic():
				return func_view(request, *args, **kwargs)
		except Exception as error:
			logger.error(f"An error {repr(error)} occurred in function view when accessing the page '{request.method} {request.get_full_path()}'")
			return HttpResponseBadRequest()

	return wrapper


class LoginRequired_WithMessage_Mixin(LoginRequiredMixin):
	"""Analogue of LoginRequiredMixin, but when redirecting add a message for user.
	Also catch exceptions in dispatch method, like ErrorTrackerView"""

	def dispatch(self, request, *args, **kwargs):
		try:
			if request.user.is_anonymous:
				messages.error(request, "To access this page, you need to log in!")
			response = super().dispatch(request, *args, **kwargs)
		except Exception as error:
			logger.error(f"An error {repr(error)} occurred in login-required generic view when accessing the page '{request.method} {request.get_full_path()}'")
			return HttpResponseBadRequest()
		else:
			return response