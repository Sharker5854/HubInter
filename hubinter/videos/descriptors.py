from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from logger import logger

class YoutubeUrl_Descriptor:
	"""This descriptor checks whether the url leads to a YouTube video"""

	def __init__(self, attr_name):
		self.attr_name = attr_name

	def __get__(self, instance, owner_class):
		return instance.__dict__[self.attr_name]

	def __set__(self, instance, value):
		value = self.__remove_url_parameters(value)
		if self._is_youtube_url(value):
			if self._id_length_is_11(value):
				instance.__dict__[self.attr_name] = value
				logger.info(f"URL for YouTube video '{value}' is correct")
			else:
				raise ValidationError(
					gettext_lazy("Video doesn't exists")
				)
		else:
			raise ValidationError(
				gettext_lazy("Your URL should lead to a YouTube video")
			)

	def _is_youtube_url(self, url):
		"""Validating provided url: does it lead to a Youtube video?"""
		url = url.strip()
		if url.startswith("https:") and "youtube.com" in url:
			return True
		else:
			return False

	def _id_length_is_11(self, url):
		"""Validating length of provided video's ID"""
		try:
			index = url.index("=")
		except:
			return False
		else:
			video_id = url[index+1:]
			if len(video_id) == 11:
				return True
			else:
				return False


	def __remove_url_parameters(self, url):
		"""If user provided url with superfluous parameters (except for "v"), delete them"""
		try:
			index = url.index("&")
		except ValueError:
			pass
		else: 
			url = url[:index]
			logger.info(f"Extra URL parameters for YouTube video '{value}' deleted")

		return url
