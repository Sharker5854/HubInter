from django import forms
from .models import Video, Theme
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

class AddVideoForm(forms.ModelForm):
	"""Form to upload your own video"""

	def clean(self):
		"""Override clean method to make some custom validation"""
		cleaned_data = self.cleaned_data
		self.is_theme_tags(cleaned_data)

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
