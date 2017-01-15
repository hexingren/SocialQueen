#!/usr/bin/python
from django import forms
from django.contrib.auth.models import User
from socialnetwork.models import *

class RegisterForm(forms.Form):
	firstname = forms.CharField(
		max_length = 20,
		label='First Name',
		required = False,
		widget=forms.TextInput(attrs={'class':'w3-group'}),
    )
	lastname = forms.CharField(
		max_length = 20,
		label='Last Name',
		required = False,
		widget=forms.TextInput(attrs={'class':'w3-group'}),
    )
	username = forms.CharField(
		max_length = 20,
		label='Username',
		widget=forms.TextInput(attrs={'class':'w3-group'}),
	)
	age = forms.IntegerField(
		label='Age',
		required = False,
		widget=forms.TextInput(attrs={'class':'w3-group'}),
	)
	bio = forms.CharField(
		max_length = 430,
		label='Bio',
		required = False,
		widget=forms.TextInput(attrs={'class':'bio-input'}),           # add attrs to widget
	)
	# email
	password1 = forms.CharField(
		max_length = 20,
		label='Password',
		widget=forms.PasswordInput(attrs={'class':'w3-group'}),
	)
	password2 = forms.CharField(
		max_length = 20,
		label='Confirm Password',
		widget=forms.PasswordInput(attrs={'class':'w3-group'}),
	)
	
	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match.")
		
		userAge = cleaned_data.get('age')
		if (userAge < 0 or userAge > 150) and (userAge != None): # hren
			raise forms.ValidationError("Age is invalid.")
		#email
		return cleaned_data
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):                 # hren
			raise forms.ValidationError("Username is already taken.")
		return username
	
class PostForm(forms.Form):
	text = forms.CharField(max_length=160, widget=forms.Textarea)
	
	def clean(self):
		cleaned_data = super(PostForm, self).clean()
		return cleaned_data
		
"""
hren
"""

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = (
			'username',
			'follow',
		)
		widgets = {'avater': forms.FileInput()} # prevent the user from deleting avater
		
	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget=forms.Textarea(attrs={'class':'bio-input'})
	
	def clean(self):
		cleaned_data = super(EditProfileForm, self).clean()
		userAge = cleaned_data.get('age')
		if (userAge < 0 or userAge > 150) and (userAge != Null): # hren
			raise forms.ValidationError("Age is invalid.")
		#email
		return cleaned_data
	

	
	


