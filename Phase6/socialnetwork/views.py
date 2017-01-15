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

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from socialnetwork.models import *
from socialnetwork.forms import *
import time
from django.core.urlresolvers import reverse

from django.core import serializers
import json # json.dumps

from s3 import s3_upload, s3_delete

# Create your views here.

@login_required
def home(request):
	context = {}
	context['username'] = request.user.username
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form'] = PostForm()
	context['lastupdate'] = time.strftime("%Y-%m-%d %H:%M:%S")
	context['profile'] = Post.profile
	context['pprofile'] = get_object_or_404(Profile, username = request.user)
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print get_object_or_404(Profile, username = request.user)
	# context['commentPhoto'] = 
	# hren
	"""
	if 'username' in request.GET:                                            
		userName = request.GET['username']
		user = User.objects.get(username=userName)
		profile = user.profileUsername.all()[0]
		context['profile'] = profile 
	"""
		
	"""
	userName = request.user.username
	user = User.objects.get(username=userName)
	profile = user.profileUsername.all()[0]
	context['profile'] = profile
	"""
	
	print "Post.profile = ", Post.profile
	#print "Post.profile.avater = ", Post.profile.avater
	return render(request, 'globalstream.html', context)

@login_required
def globalstream(request):
	context = {}
	context['username'] = request.user.username
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form'] = PostForm()
	context['lastupdate'] = time.strftime("%Y-%m-%d %H:%M:%S")
	context['profile'] = Post.profile
	context['pprofile'] = get_object_or_404(Profile, username = request.user)
	print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	print get_object_or_404(Profile, username = request.user)
	# hren
	"""
	if 'username' in request.GET:                                            
		userName = request.GET['username']
		user = User.objects.get(username=userName)
		profile = user.profileUsername.all()[0]
		context['profile'] = profile 
	"""
		
	"""
	userName = request.user.username
	user = User.objects.get(username=userName)
	profile = user.profileUsername.all()[0]
	context['profile'] = profile
	"""
	
	for p in Post.objects.all().order_by('-timeline'):
		print "post", p.id
		print "   ", p.profile
	
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
		
		user = User.objects.get(username=userName)   # if it's the only one, use objects.get instead of objects.filter

		profile = Profile.objects.get(username=user)
		#profile = user.profileUsername.all()[0]
		context['username'] = userName                    # context['username'] = user.username                      
		context['firstname'] = profile.first_name
		context['lastname'] = profile.last_name
		context['posts'] = posts
		context['avater'] = profile.avater
		context['age'] = profile.age
		context['bio'] = profile.bio
		context['profile'] = profile
		context['pprofile'] = get_object_or_404(Profile, username = request.user)
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
	
	# At this point, the form data is valid. Register and login the user.
	new_user = User.objects.create_user(
	                                    username=form.cleaned_data['username'],
										 password=form.cleaned_data['password1'],
										 email=form.cleaned_data['email'])
	# Mark the user as inactive to prevent login before email confirmation.
	new_user.is_active = False
	new_user.save()
	
	# Generate a one-time user token and an email message body
	token = default_token_generator.make_token(new_user)
	
	email_body = """
Welcome to SocialQueen. Please click the link below to verify your email address and complete the registration of your account: http://%s%s """ % (request.get_host(),
									 reverse('confirm', args=(new_user.username, token)))
									
	send_mail(subject="Verify your email address",
			   message=email_body,
			   from_email="hren@andrew.cmu.edu",
			   recipient_list=[new_user.email])	
	
	context['email'] = form.cleaned_data['email']
		
	new_profile = Profile(
		                  username=new_user,                            # username is ForeignKey, not a CharField [models.py]
		                  first_name=form.cleaned_data['firstname'],
						  last_name=form.cleaned_data['lastname'],
						  age=form.cleaned_data['age'],
						  bio=form.cleaned_data['bio'],)
						  #email)
	new_profile.save()
	
	return render(request, 'needs-confirmation.html', context)
	
	
"""
	new_user = authenticate(username=form.cleaned_data['username'],   # hren
							password=form.cleaned_data['password1'])
	login(request, new_user)
	return redirect(reverse('globalstream'))
"""

@transaction.atomic
def confirm_registration(request, username, token):
	user = get_object_or_404(User, username=username)
	
	# Send 404 error if token is invalid
	if not default_token_generator.check_token(user, token):
		raise Http404
		
	# Otherwise token was valid, activate the user.
	user.is_active = True
	user.save()
	return render(request, 'confirmed.html', {})
		
	
	
@login_required
@transaction.atomic
def Postmsg(request):
	#print "hello"
	context = {}
	if request.method == 'GET':
		context['form'] = PostForm()
		context['posts'] = Post.objects.all().order_by('-timeline')  #hren
		print "ddddddddddddddddddddddddddddddddddddddddddddd"
		return render(request, 'globalstream.html', context)
	form = PostForm(request.POST)
	context['form'] = form
	if not form.is_valid():
	
		posts = Post.objects.all().order_by('-timeline')
		context['posts'] = posts
		return render(request, 'globalstream.html', context)
	new_post = Post(text=form.cleaned_data['text'],username = request.user.username, timeline = time.strftime("%Y-%m-%d %H:%M:%S"), profile=get_object_or_404(Profile, username = request.user))
	print'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	print new_post.profile
	#new_post = Post(text=form.cleaned_data['text'],username = request.user.username, timeline = form.cleaned_data['timeline'])
	new_post.save()
	context['posts'] = Post.objects.all().order_by('-timeline')
	context['form']=PostForm()
	context['lastupdate'] = time.strftime("%Y-%m-%d %H:%M:%S")
	context['username'] = request.user.username   # hren note: each function in view.py corresponds to a url (a web page), if you need the values of some variables to display on that page, you need to put the variables in the context[""];
	context['pprofile'] = get_object_or_404(Profile, username = request.user)
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
	content_type = guess_type(profile.avater)
	return HttpResponse(profile.avater, content_type=content_type) # hren Jeff's example, not video version

@login_required
@transaction.atomic
def EditProfile(request):
	context = {}
	userName = request.user.username
	context['username'] = userName
	user = get_object_or_404(User, username=userName)
	
	
	if request.method == "GET":
		profile = Profile.objects.get(username=user)
		#profile = user.profileUsername.all()[0]
		context['form'] = EditProfileForm(instance=profile)
		return render(request, 'editprofile.html', context)
	
	profile = Profile.objects.select_for_update().get(username=request.user)
	# hren
	print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
	print profile.id
	context['profile'] = profile
	form = EditProfileForm(request.POST, request.FILES, instance=profile)
	context['form'] = form
	if not form.is_valid():
		return render(request, 'editprofile.html', context)
	
	if form.cleaned_data['avater']:
		url = s3_upload(form.cleaned_data['avater'], profile.id)
		profile.avater = url
		profile.save()
		print (profile.avater)
	
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
	context['username'] = request.user.username
	context['posts'] = followedPost
	context['form'] = PostForm()
	context['lastupdate'] = time.strftime("%Y-%m-%d %H:%M:%S")
	# hren
	userName = request.user.username
	user = User.objects.get(username=userName)
	#profile = user.profileUsername.all()[0]
	context['pprofile'] = get_object_or_404(Profile, username = request.user)
	return render(request, 'followstream.html', context)

@login_required
def save_comment(request):
	usernamePost = request.GET['usernamePost']
	timelinePost = request.GET['timelinePost']
	usernameComment = request.GET['usernameComment']
	timelineComment = request.GET['timelineComment']
	textComment = request.GET['textComment']
	commentPhoto = request.GET['commentPhoto']
	print "commentPhoto: " + commentPhoto 
	newComment = Comment(text=textComment, username=usernameComment, timeline=timelineComment, commentPhoto=commentPhoto)
	newComment.save()
	postbelongto = get_object_or_404(Post, username=usernamePost, timeline=timelinePost)
	postbelongto.comment.add(newComment)
	return HttpResponse(status=200, content_type="text/plain")
	#return HttpResponse(status=200, content_type="text/plain") # http://stackoverflow.com/questions/622481/django-ajax  hren
	
@login_required
def get_globalstream_newpostonly_json(request):
	if 'lastupdate' in request.GET:
		# https://docs.djangoproject.com/en/1.9/ref/models/querysets/
		lastupdate = request.GET['lastupdate']
		print lastupdate
		posts = Post.objects.filter(timeline__gt=lastupdate).order_by('-timeline')
		print posts
		response_text = serializers.serialize('json', posts)
		print response_text
		lastupdate = time.strftime("%Y-%m-%d %H:%M:%S") # http://stackoverflow.com/questions/9648861/return-multiple-variables-from-an-django-ajax-function
		print lastupdate
		data = json.dumps({
			'response_text': response_text,
			'lastupdate': lastupdate,
		})
		print data
		
	return HttpResponse(data, content_type='application/json')


	

	


		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
