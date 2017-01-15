from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from socialnetwork.models import *
from socialnetwork.forms import *
import time

# Create your views here.
"""
def login(request):
	context = {}
	
	if request.method == 'POST':
		context['form'] = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			return redirect('socialnetwork/globalstream/')
	else:
		context['form'] = LoginForm()
	return render(request, 'login.html', {'form': form})
"""

@login_required
def home(request):
	context = {}
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form'] = PostForm()
	return render(request, 'globalstream.html', context)
	
	
@login_required
def globalstream(request):
	context = {}
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form'] = PostForm()
	return render(request, 'globalstream.html', context)
	
	

	
@login_required
def profile(request):
	context = {}
	if 'username' in request.GET:                                            # POST?
		userName = request.GET['username']                                   # delete
		userData = User.objects.filter(username=userName)
		posts = Post.objects.filter(username=userName).order_by('-timeline')
		if userData:
			user = userData[0]
			context['username'] = userName                    # context['username'] = user.username                      
			context['firstname'] = user.first_name
			context['lastname'] = user.last_name
			context['posts'] = posts
	return render(request, 'profile.html', context)
		
@transaction.atomic
def register(request):
	context = {}
	
	if request.method == 'GET':
		context['form'] = RegisterForm()
		return render(request, 'register.html', context)
	
	form = RegisterForm(request.POST)
	context['form'] = form
	
	if not form.is_valid():
		return render(request, 'register.html', context)
	
	new_user = User.objects.create_user(first_name=form.cleaned_data['firstname'],
										 last_name=form.cleaned_data['lastname'],
	                                    username=form.cleaned_data['username'],
										 password=form.cleaned_data['password1'],)
	new_user.save()

	new_user = authenticate(username=form.cleaned_data['username'],
							password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect('/globalstream/')
	
	
@login_required
@transaction.atomic
def Postmsg(request):
	print "hello"
	context = {}
	if request.method == 'GET':
		context['form'] = PostForm()
		context['posts'] = Post.objects.all().order_by('-timeline')
		print context
		return render(request, 'globalstream.html', context)
	form = PostForm(request.POST)
	context['form'] = form
	if not form.is_valid():
	
		posts = Post.objects.all().order_by('-timeline')
		context['posts'] = posts
		return render(request, 'globalstream.html', context)
	new_post = Post(text=form.cleaned_data['text'],username = request.user.username, timeline = time.strftime("%b %d %Y %H:%M:%S"))
	new_post.save()
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form']=PostForm()
	return render(request, 'globalstream.html', context)
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
