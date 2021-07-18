from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from .models import Video, YoutubeVideo
from .utils import YT_Video_DataParser


class AddVideoForm(forms.ModelForm):
	"""Form to upload your own video"""

	def clean(self):
		"""Override clean method to make some custom validation"""
		self.is_theme_tags(self.cleaned_data)

	def is_theme_tags(self, data):
		"""Validating whether the selected tags belong to the selected theme"""
		for tag in data['tags']:
			if tag.theme != data['theme']:
				raise ValidationError(
					gettext_lazy('The {} tag does not relate to the {} theme.'.format(tag, data['theme']))
				)

	class Meta:
		model = Video
		fields = ('title', 'description', 'theme', 'tags', 'preview', 'video', 'is_published')
		widgets = {
			'title' : forms.TextInput(
        		attrs={
        			'class' : 'margin-20',
        			'placeholder' : 'Title...',
        		}
        	),
        	'description' : forms.Textarea(
        		attrs={
        			'class' : 'margin-50',
        			'placeholder' : 'Description...',
        			'rows' : 8,
        			'cols' : 40
        		}
        	),
        	'theme' : forms.Select(
        		attrs={
        			'class' : 'margin-20',
        		}
        	),
        	'tags' : forms.SelectMultiple(
        		attrs={
        			'class' : 'margin-50',
        		}
        	),
        	'preview' : forms.FileInput(
        		attrs={
        			'class' : 'margin-20',
        		}
        	),
        	'video' : forms.FileInput(
        		attrs={
        			'class' : 'margin-50',
        		}
        	),
        	'is_published' : forms.CheckboxInput(
        		attrs={
        			'style' : 'width: 15px; margin-top: 10px;',
        			'class' : 'margin-50',
        			'default' : True,
        		}
        	)
        }
		labels = {
			'title' : '',
			'description' : '',
			'theme' : 'Video Theme',
			'tags' : 'Tags (hold down “Control” to select more than one)',
			'preview' : 'Preview',
			'video' : 'Video',
			'is_published' : 'Publish Now'
		}




class AddYoutubeVideoForm(forms.ModelForm):
	"""Form to add your video from YouTube on site"""

	def clean(self):
		self.is_theme_tags(self.cleaned_data)
		try:
			parser = YT_Video_DataParser(self.cleaned_data['iframe_code']) #!!! At this stage, this field contains the URL to the video, NOT iframe CODE !!!
		except ValidationError:
			raise
		else:
			parser.get_iframe_code() # save the iframe code in attribute before sending it to the server, to immediately raise a ValidationError in the form
			self.cleaned_data['parser'] = parser

	def is_theme_tags(self, data):
		"""Validating whether the selected tags belong to the selected theme"""
		for tag in data['tags']:
			if tag.theme != data['theme']:
				raise ValidationError(
					gettext_lazy('The {} tag does not relate to the {} theme.'.format(tag, data['theme']))
				)

	class Meta:
		model = YoutubeVideo
		fields = ('iframe_code', 'theme', 'tags')
		widgets = {
			'iframe_code' : forms.TextInput(
        		attrs={
        			'class' : 'margin-20',
        			'placeholder' : 'Provide link to YouTube video...',
        		}
        	),
        	'theme' : forms.Select(
        		attrs={
        			'class' : 'margin-20',
        		}
        	),
        	'tags' : forms.SelectMultiple(
        		attrs={
        			'class' : 'margin-50',
        		}
        	)
        }
		labels = {
			'iframe_code' : '',
			'theme' : 'YouTube Video Theme',
			'tags' : 'Tags (hold down “Control” to select more than one)',
		}
