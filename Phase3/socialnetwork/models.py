
from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    text = models.CharField(max_length=160)
    username = models.CharField(max_length=20)
    # timeline = models.DateTimeField(auto_now_add=True)
    timeline = models.CharField(max_length=20)
    """
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()
    """
    def __str__(self):
        return self.text
   

	


# class Profile(models.Model):
#	 name = models.CharField(max_length=20)
#	 user = models.ForeignKey(User)

#	 about_me = models.CharField(max_length=500)


