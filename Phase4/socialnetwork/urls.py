"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
# from django.conf.urls import include, url
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views as private_views

urlpatterns = [
    url(r'^$', private_views.home, name='home'),
    url(r'^login', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout', auth_views.logout_then_login, name='logout'),
    url(r'^register', private_views.register, name='register'),
    url(r'^globalstream', private_views.globalstream, name='globalstream'),
    url(r'^profile', private_views.profile, name='profile'),
    url(r'^Postmsg', private_views.Postmsg, name='Postmsg'),
    #url(r'^globalstream', private_views.Postmsg, name='Postmsg'),
    url(r'^followstream', private_views.followstream, name='followstream'),
    url(r'^editprofile', private_views.EditProfile, name='editprofile'),
    #url(r'^uploadavater', private_views.UploadAvater, name='uploadavater'),
    url(r'^uploadavater', private_views.UploadAvater, name='uploadavater'),
    url(r'^follow', private_views.follow, name='follow'),
    url(r'^unfollow', private_views.unfollow, name='unfollow'),
    url(r'^get_globalstream_newpostonly_json', 'socialnetwork.views.get_globalstream_newpostonly_json', name='ggnj'),
    url(r'^save_comment', 'socialnetwork.views.save_comment', name='save_comment'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', private_views.confirm_registration, name='confirm'),    
]
# checked
