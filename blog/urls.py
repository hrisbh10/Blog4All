"""Blog4All URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "blog"

urlpatterns = [
	path("",views.homepage,name="homepage"),
	path("register/",views.register,name="register"),
	path("login/",views.login_request,name="login"),
	path("logout/",views.logout_request,name="logout"),
    path('blog/<single_slug>/',views.blogpage,name="blogpage"),
    path('profile/<user>/',views.profile,name="profile"),
    path('addblog/',views.add_blog,name="addblog"),
]
