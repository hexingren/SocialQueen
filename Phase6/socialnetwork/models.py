from django.db import models
from django.contrib.auth.models import User
"""
User is a class in django.contrib.auth.models. In User, there are many fields,
like 'username', 'first_name', 'last_name'.
"""
from django import forms

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, related_name="profileUsername") # https://docs.djangoproject.com/es/1.9/ref/models/fields/
    #username = models.ForeignKey(User, related_name="profileUsername")
    first_name = models.CharField(max_length=20, blank=True, null=True) # http://stackoverflow.com/questions/26727616/not-null-constraint-failed-error
    last_name = models.CharField(max_length=20, blank=True, null=True) 
    age = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=430, blank=True, null=True)
    # avater = models.ImageField(upload_to="avaterImg", blank=True, null=True) # if using ImageField, we need Pillow.
    avater = models.CharField(max_length=256, blank=True, null=True)
    follow = models.ManyToManyField(User)
    #content_type = models.CharField(max_length=50)
    #email
    # mac probably should user__exact ==> username__exact
    
    @staticmethod
    def get_user_profile_with_id(id):
        return Profile.objects.filter(username__exact=User.objects.filter(id__exact=id))[0]

class Comment(models.Model):
    text = models.CharField(max_length=160)
    username = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    commentPhoto = models.CharField(max_length=60, default='')
    #timeline = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    # user = models.ForeignKey(User)
    text = models.CharField(max_length=160)
    username = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    # timeline = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comment)
    # mac
    profile = models.ForeignKey(Profile, null=True)
    def __str__(self):
        return self.text
        
"""
hren
"""
    



    


