from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type       # hren used in video, not in Jeff's example

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from socialnetwork.models import *
from socialnetwork.forms import *
import time
from django.core.urlresolvers import reverse

# Create your views here.

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
	if 'username' in request.GET:                                            
		userName = request.GET['username']
		profileUsername = get_object_or_404(User, username=userName)                                   
		# if
		loggedinProfile = get_object_or_404(Profile, username = request.user)
		followed = loggedinProfile.follow.all()
		if profileUsername in followed:
			context['unFollowOption'] = True
		
		posts = Post.objects.filter(username=userName).order_by('-timeline')
		
		user = User.objects.get(username=userName)

		profile = user.profileUsername.all()[0]
		context['username'] = user.username                    # context['username'] = userName                      
		context['firstname'] = profile.first_name
		context['lastname'] = profile.last_name
		context['posts'] = posts
		context['avater'] = profile.avater
		context['age'] = profile.age
		context['bio'] = profile.bio
		#email
		if userName == request.user.username:
			context['editOption'] = True
		return render(request, 'profile.html', context)
		
	return render(request, 'profile.html', context)           # error messages

# replace line 53
"""
userData = User.objects.filter(username=userName)
if not userData:
	context['errors'] = 'User does not exist.'
	return render(request, 'profile.html', context)
else:
	user = userData[0]
"""
		
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
	
	new_user = User.objects.create_user(
	                                    username=form.cleaned_data['username'],
										 password=form.cleaned_data['password1'],)
	new_user.save()
	
	new_profile = Profile(
		                  username=new_user,                            # username is ForeignKey, not a CharField [models.py]
		                  first_name=form.cleaned_data['firstname'],
						  last_name=form.cleaned_data['lastname'],
						  #email
						  age=form.cleaned_data['age'],
						  bio=form.cleaned_data['bio'],)
	new_profile.save()
	new_user = authenticate(username=form.cleaned_data['username'],   # hren
							password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('globalstream'))
	
	
@login_required
@transaction.atomic
def Postmsg(request):
	#print "hello"
	context = {}
	if request.method == 'GET':
		context['form'] = PostForm()
		context['posts'] = Post.objects.all().order_by('-timeline')  #hren
		return render(request, 'globalstream.html', context)
	form = PostForm(request.POST)
	context['form'] = form
	if not form.is_valid():
	
		posts = Post.objects.all().order_by('-timeline')
		context['posts'] = posts
		return render(request, 'globalstream.html', context)
	new_post = Post(text=form.cleaned_data['text'],username = request.user.username, timeline = time.strftime("%b %d %Y %H:%M:%S"))
	#new_post = Post(text=form.cleaned_data['text'],username = request.user.username, timeline = form.cleaned_data['timeline'])
	new_post.save()
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form']=PostForm()
	return render(request, 'globalstream.html', context)
"""
hren 
request is an object in django framework. user is a field in request.
request.user is just like request.GET, request.POST, request.FILES
User is a class in django.contrib.auth.models
"""

	
"""
hren update
"""

@login_required
def UploadAvater(request):
	userName = request.GET['username']
	user = get_object_or_404(User, username=userName) # in User, username is a Charfield, it's a field
	profile = get_object_or_404(Profile, username=user) # in Profile, username is a ForeignKey, it's an object
	if not profile.avater:
		raise Http404
	content_type = guess_type(profile.avater.name)
	return HttpResponse(profile.avater, content_type=content_type) # hren Jeff's example, not video version

@login_required
def EditProfile(request):
	context = {}
	userName = request.user.username
	context['username'] = userName
	user = get_object_or_404(User, username=userName)
	
	if request.method == "GET":
		profile = user.profileUsername.all()[0]
		context['form'] = EditProfileForm(instance=profile)
		return render(request, 'editprofile.html', context)
	
	profile = Profile.objects.select_for_update().get(username=request.user)
	form = EditProfileForm(request.POST, request.FILES, instance=profile)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'editprofile.html', context)
	
	form.save()
	return redirect(reverse('profile') + '?username=' + request.user.username)
"""
hren
instance is a field in ModelForm (ModelForm is a class)
profile is a corresponding model of ModelForm
form is an object of ModelForm
ProjectEditForm is a constructor of ModelForm
"""
	
@login_required
def follow(request):
	if 'username' in request.GET:
		userName = request.GET['username']
		profileUsername = get_object_or_404(User, username=userName)
		loggedinProfile = get_object_or_404(Profile, username=request.user)
		loggedinProfile.follow.add(profileUsername)
	return redirect(reverse('profile') + '?username=' + userName)               # profile hren

@login_required
def unfollow(request):
	if 'username' in request.GET:
		userName = request.GET['username']
		profileUsername = get_object_or_404(User, username=userName)
		loggedinProfile = get_object_or_404(Profile, username=request.user)
		loggedinProfile.follow.remove(profileUsername)
	return redirect(reverse('profile') + '?username=' + userName)                 # profile hren
 
@login_required
def followstream(request):
	context = {}
	followedList = []
	followedPost = []
	
	loggedinProfile = get_object_or_404(Profile, username=request.user)
	followedUsers = loggedinProfile.follow.all()
	posts = Post.objects.all().order_by('-timeline')
	
	for user in followedUsers:
		followedList.append(user.username)
	
	for post in posts:                                                # hren find followed posts
		if post.username in followedList:
			followedPost.append(post)
	
	context['posts'] = followedPost
	return render(request, 'followstream.html', context)
	


		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
