from django.db import models
from django.contrib.auth.models import User
"""
User is a class in django.contrib.auth.models. In User, there are many fields,
like 'username', 'first_name', 'last_name'.
"""
from django import forms

# Create your models here.
class Comment(models.Model):
    text = models.CharField(max_length=160)
    username = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    #timeline = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    text = models.CharField(max_length=160)
    username = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    #timeline = models.DateTimeField(auto_now_add=True)
    comment = models.ManyToManyField(Comment)
    def __str__(self):
        return self.text
        
"""
hren
"""
class Profile(models.Model):
    username = models.ForeignKey(User, related_name="profileUsername") # https://docs.djangoproject.com/es/1.9/ref/models/fields/
    first_name = models.CharField(max_length=20, blank=True, null=True) # http://stackoverflow.com/questions/26727616/not-null-constraint-failed-error
    last_name = models.CharField(max_length=20, blank=True, null=True) 
    age = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=430, blank=True, null=True)
    avater = models.ImageField(upload_to="avaterImg", blank=True, null=True) # if using ImageField, we need Pillow.
    follow = models.ManyToManyField(User)
    #content_type = models.CharField(max_length=50)
    #email



    


