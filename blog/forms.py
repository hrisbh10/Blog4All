from django import forms
from django.contrib.auth.models import User
from .models import Blog
from django.contrib.auth.forms import UserCreationForm
from tinymce.widgets import TinyMCE

class NewUserForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50,required=False)
	class Meta:
		model = User
		fields = ['first_name','last_name','email','username','password1','password2']

	def save(self,commit=True):
		user = super(NewUserForm,self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user

class NewBlogForm(forms.ModelForm):
	blog_title = forms.CharField(max_length=200,help_text="The Header of your Blog")
	blog_content = forms.CharField(widget=TinyMCE(attrs={'cols':80,'rows':40}))

	class Meta:
		model = Blog
		fields = ['blog_title','blog_content']

	def save(self,user,commit=True):
		blog = super(NewBlogForm,self).save(commit=False)
		blog.publisher = user

		if commit:
			blog.save()
		return blog



	