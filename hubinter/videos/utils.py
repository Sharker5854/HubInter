from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.http import FileResponse

from .descriptors import YoutubeUrl_Descriptor
from yt_iframe import yt
import requests
import urllib
import tempfile
import json
import uuid


class YT_Video_DataParser:
	"""Parser for YouTube-video-data by URL"""
	url = YoutubeUrl_Descriptor('url')

	def __init__(self, url):
		self.url = url


	def get_iframe_code(self):
		"""Set attribute 'iframe' with HTML-code generated by provided link"""
		try:
			iframe = yt.video(self.url, width="1280", height="720")
		except yt.InvalidLink:
			raise ValidationError("Your URL is incorrect")
		else:
			self.iframe = iframe


	def get_preview_file(self):
		"""Get preview file and return TemporaryFile with it"""
		response = requests.get(self.get_preview_url(), stream=True)

		if response.status_code == requests.codes.ok:
			file = tempfile.TemporaryFile()
			file.write(response.content)
		else:
			file = None

		return file


	def get_title(self):
		"""Get json of video data by request to 'oembed' according to the provided URL"""
		params = {
			"format" : 'json',
			"url" : "https://www.youtube.com/watch?v={}".format(self.video_id)
		}
		url = "https://youtube.com/oembed"
		query_string = urllib.parse.urlencode(params)
		url = url + "?" + query_string

		try:
			with urllib.request.urlopen(url) as response:
				response_text = response.read()
				data = json.loads(response_text.decode())
		except: # if video with provided ID doesn't exist, iframe will be unavailavle and the title will be appropriate...
			return "Error. Incorrect YouTube URL provided_" + str(uuid.uuid4())[:5]
		else:
			return data['title']


	@property
	def video_id(self):
		index = self.url.index("=")
		return self.url[index+1:]


	def get_preview_url(self):
		"""Helper method: return URL to the video's preview according to ID"""
		return "https://img.youtube.com/vi/{}/maxresdefault.jpg".format(self.video_id)







def get_author_info(video_obj, context):
	"""Get author's avatar-url, username and subs"""
	if context['video_type'] == "uploaded":
		context['author_object'] = video_obj.author
		context['author_avatar'] = video_obj.author.avatar.url
		context['author_username'] = video_obj.author.username
		context['author_subscribers'] = video_obj.author.subscribers_amount
	elif context['video_type'] == "youtube":
		context['author_object'] = video_obj.added_by
		context['author_avatar'] = video_obj.added_by.avatar.url
		context['author_username'] = video_obj.added_by.username
		context['author_subscribers'] = video_obj.added_by.subscribers_amount
	return context
