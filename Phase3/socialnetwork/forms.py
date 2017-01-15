#!/usr/bin/python
from django import forms
from django.contrib.auth.models import User

"""
class LoginForm(forms.Form):
	username = forms.CharField(
		max_length = 20,
		widget=forms.TextInput(attrs={'class':'w3-group'}),
	)
	password = forms.CharField(
		max_length = 20,
		label='Password',
		widget=forms.PasswordInput(attrs={'class':'w3-group'}),
	)
"""

class RegisterForm(forms.Form):
	firstname = forms.CharField(
		max_length = 20,
		label='First Name',
		widget=forms.TextInput(attrs={'class':'w3-group'}),
    )
	lastname = forms.CharField(
		max_length = 20,
		label='Last Name',
		widget=forms.TextInput(attrs={'class':'w3-group'}),
    )
	username = forms.CharField(
		max_length = 20,
		label='Username',
		widget=forms.TextInput(attrs={'class':'w3-group'}),
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
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")
		return username
	
class PostForm(forms.Form):
	text = forms.CharField(max_length=160, widget=forms.Textarea)
	
	def clean(self):
		cleaned_data = super(PostForm, self).clean()
		return cleaned_data
	
	


