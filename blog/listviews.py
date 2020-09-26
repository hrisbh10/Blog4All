from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .models import Blog,Comment

def pageObject(request,blogs):
	num_blogs = 7
	page = request.GET.get('page')
	paginator = Paginator(blogs,num_blogs) #number of blogs per page
	page_obj = paginator.get_page(page)
	return page_obj

def homepage(request):
	blogs = Blog.objects.order_by('-blog_published')
	page_obj = pageObject(request,blogs)
	if page_obj.number == 1:
		return render(request,"blog/home.html",{"blogs":page_obj,"info":blogs.last()})
	return render(request,"blog/home.html",{"blogs":page_obj})

def blogpage(request,single_slug):
	blog = get_object_or_404(Blog,blog_slug=single_slug)
	comments = blog.main_thread.get_comments()
	return render(request,"blog/blogpage.html",{"blog":blog,"comments":comments})

def profile(request,user):
	user = get_object_or_404(User,username=user)
	matching_blogs = Blog.objects.filter(publisher=user).order_by('-blog_published')
	return render(request,"blog/profile.html",{"profile":user,"blogs":matching_blogs})

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
		page_obj = pageObject(request,matching_blogs.order_by('-blog_published'))
		return render(request, 'blog/search.html',{"query":query,"blogs":page_obj})

	return HttpResponse("Enter valid search keyword")