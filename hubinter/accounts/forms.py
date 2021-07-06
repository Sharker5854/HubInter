from django import forms
from django.contrib.auth.forms import (
	AuthenticationForm, UserCreationForm, 
	PasswordChangeForm, PasswordResetForm, SetPasswordForm
)

from .models import User



class LoginForm(AuthenticationForm):
	username = forms.CharField(max_length=100, min_length=3, label='', 
		widget=forms.TextInput(
			attrs= {
				'class' : 'margin-10',
				'placeholder' : 'Username...',
			}
		)
	)
	password = forms.CharField(max_length=255, min_length=4, label='', 
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-10',
				'placeholder' : 'Password...',
			}
		)
	)

	def __init__(self, request, *args, **kwargs):
		'''Simply do not pass 'request' arg to the parent'''
		super().__init__(*args, **kwargs)	

	class Meta(AuthenticationForm):
		model = User
		fields = ('username', 'password')




class RegisterForm(UserCreationForm):
	name = forms.CharField(max_length=100, min_length=2, label='', help_text='',
		widget=forms.TextInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Your name...',
			}
		)
	)
	email = forms.CharField(max_length=100, min_length=2, label='', help_text='',
		widget=forms.EmailInput(
			attrs= {
				'class' : 'margin-50',
				'placeholder' : 'Your e-mail...',
			}
		)
	)
	username = forms.CharField(max_length=100, min_length=3, label='', help_text='',
		widget=forms.TextInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Username...',
			}
		)
	)
	password1 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Password...',
			}
		)
	)
	password2 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Confirm password...',
			}
		)
	)

	class Meta(UserCreationForm):
		model = User
		fields = ('name', 'email', 'username', 'password1', 'password2')




class ChangePasswordForm(PasswordChangeForm):
	old_password = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-40',
				'placeholder' : 'Your old password...',
			}
		)
	)
	new_password1 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'New password...',
			}
		)
	)
	new_password2 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Confirm new password...',
			}
		)
	)




class ResetPasswordForm(PasswordResetForm):
	email = forms.EmailField(label='', help_text='',
		widget=forms.EmailInput(
			attrs={
				'class' : 'margin-20',
				'placeholder' : 'Enter your e-mail...',
			}
		)
	)




class ResetPasswordConfirmForm(SetPasswordForm):
	new_password1 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'New password...',
			}
		)
	)
	new_password2 = forms.CharField(max_length=100, min_length=4, label='', help_text='',
		widget=forms.PasswordInput(
			attrs= {
				'class' : 'margin-20',
				'placeholder' : 'Confirm new password...',
			}
		)
	)