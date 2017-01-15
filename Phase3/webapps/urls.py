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
from django.conf.urls import include, url
from socialnetwork import views
from socialnetwork import views as private_views

urlpatterns = [
    url(r'^$', private_views.home),
    url(r'^', include('socialnetwork.urls')),
]
"""

urlpatterns = [
    url(r'^$', private_views.home, name='home'),
    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', private_views.register, name='register'),
    url(r'^globalstream$', private_views.globalstream, name='globalstream'),
    url(r'^profile$', private_views.profile, name='profile'),
]
"""
