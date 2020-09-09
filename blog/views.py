from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog
from .forms import NewUserForm, NewBlogForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
	if request.method == 'POST':
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data['username']
			messages.success(request, f"New Account Created: {username}")
			login(request,user)
			return redirect("blog:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request,f"{msg}: {form.error_messages[msg]}")

			return render(request,'blog/register.html',{"form":form})

	form = NewUserForm()
	return render(request,'blog/register.html',{"form":form})

def login_request(request):
	if request.user.is_authenticated:
		messages.info(request,"You are already logged in! Logout first")
		return redirect("blog:homepage")

	if request.method == 'POST':
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)

			if user is not None:
				login(request,user)
				messages.success(request,f"Successfully logged in as {username}")

				if request.GET['next']:
					return redirect(request.GET['next'])

				return redirect("blog:homepage")
			else:
				messages.error(request,"Invalid username or password")
				
		else:
			messages.error(request,"Invalid username or password")


	form = AuthenticationForm()
	return render(request,'blog/login.html',{"form":form})

def logout_request(request):
	logout(request)
	messages.info(request,"Logout Successful")
	if request.GET['next']:
		return redirect(request.GET['next'])
	return redirect("blog:homepage")


@login_required(login_url="blog:login")
def add_blog(request):
	if not request.user.is_authenticated:
		messages.error(request,"Login into your account first")
		return redirect("blog:homepage")

	if request.method == 'POST':
		form = NewBlogForm(request.POST)
		if form.is_valid():
			blog = form.save(request.user)

			messages.success(request,"Successfully Created a new blog")
			return redirect("blog:blogpage", blog.blog_slug)
		else:
			messages.error(request,"Some fields may be missing")
			return render(request,'blog/add_blog.html',{'form':form})


	form = NewBlogForm()
	return render(request,'blog/add_blog.html',{'form':form})

@login_required(login_url="blog:login")
def edit_blog(request,single_slug):
	blog = get_object_or_404(Blog,blog_slug=single_slug)
	if (blog.publisher != request.user):
		messages.error(request,"Login into your account first")
		return redirect("blog:homepage")

	if request.method == 'POST':
		form = NewBlogForm(request.POST,instance=blog)
		if form.is_valid():
			form.modify()
			messages.success(request,"Successfully modified your blog")
			return redirect("blog:blogpage", blog.blog_slug)

		else:
			messages.error(request,"Unable to process your request")
			return render(request,'blog/add_blog.html',{'form':form})


	form = NewBlogForm(instance=blog)
	return render(request,'blog/add_blog.html',{'form':form})

@login_required(login_url="blog:login")
def delete(request,id):
	blog = get_object_or_404(Blog,id=id)
	if (blog.publisher != request.user):
		messages.error(request,"Invalid Action")
		return redirect("blog:homepage")
	user = blog.publisher;
	blog.delete()

	return redirect("blog:profile",user)
