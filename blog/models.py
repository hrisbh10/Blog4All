from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
# Create your models here.

class Blog(models.Model):
	blog_title = models.CharField(max_length=200)
	publisher = models.ForeignKey(User,on_delete=models.CASCADE)
	blog_published = models.DateTimeField(default=timezone.now,verbose_name="date published")
	blog_content = models.TextField()

	blog_slug = models.CharField(max_length=200,default=1)

	def __str__(self):
		return self.blog_title

	def save(self,*args,**kwargs):
		if not self.id: #Newly created or not
			self.blog_slug = slugify(f"{self.publisher} {self.blog_title} {randint(1,1147483647)}")

		super(Blog,self).save(*args,**kwargs)

