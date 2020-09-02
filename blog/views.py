from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog
from .forms import NewUserForm, NewBlogForm
from django.db.models import Q

# Create your views here.

def homepage(request):
	return render(request,"blog/home.html",{"blogs":Blog.objects.order_by('-blog_published')})

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
	if request.method == 'POST':
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				messages.success(request,f"Successfully logged in as {username}")
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
	return redirect("blog:homepage")

def blogpage(request,single_slug):
	try:
		blog = Blog.objects.filter(blog_slug=single_slug).get()
	except Blog.DoesNotExist:
		messages.error(request, "Blog Not Found")
		return redirect("blog:homepage")
	return render(request,"blog/blogpage.html",{"blog":blog})


def profile(request,user):
	try:
		user = User.objects.filter(username=user).get()
		matching_blogs = Blog.objects.filter(publisher=user).order_by('-blog_published')
		return render(request,"blog/profile.html",{"profile":user,"blogs":matching_blogs})
		
	except User.DoesNotExist:
		messages.error(request, "Invalid Username")
		return redirect("blog:homepage")

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

def edit_blog(request,single_slug):
	try:
		blog = Blog.objects.filter(blog_slug=single_slug).get()
		if blog.publisher != request.user:
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

	except Blog.DoesNotExist:
		messages.error(request, "Blog Not Found")
		return redirect("blog:homepage")

def delete(request,id):
	blog = Blog.objects.get(id=id)
	user = blog.publisher;
	blog.delete()

	return redirect("blog:profile",user)

def search(request):
	query = ""
	if ('q' in request.GET) and (request.GET['q'].strip()):
		query = request.GET['q'].strip()
		matching_blogs = Blog.objects.filter(
							Q(blog_title__icontains=query)|
							Q(blog_content__icontains=query)|
							Q(publisher__username__icontains=query)|
							Q(publisher__first_name__icontains=query)|
							Q(publisher__last_name__icontains=query)
						)
		return render(request, 'blog/search.html',{"query":query,"blogs":matching_blogs.all()})

	return HttpResponse("Enter valid search keyword")