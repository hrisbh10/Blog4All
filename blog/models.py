from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from random import randint
# Create your models for Blog4All-HR here.


class CommentThread(models.Model):

	def get_comments(self):
		result = []
		comments = Comment.objects.filter(parent=self)
		for comment in comments:
			tree = {}
			tree['main'] = comment
			child = comment.get_comments()
			if child:
				tree['child'] = child
			result.append(tree)
		return result


class Blog(models.Model):
	blog_title = models.CharField(max_length=200)
	publisher = models.ForeignKey(User,on_delete=models.CASCADE)
	blog_published = models.DateTimeField(default=timezone.now,verbose_name="date published")
	blog_content = models.TextField()
	blog_slug = models.CharField(max_length=200,default=1)

	main_thread = models.OneToOneField(CommentThread,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.blog_title

	def save(self,*args,**kwargs):
		if not self.id: #Newly created or not
			self.blog_slug = slugify(f"{self.publisher} {self.blog_title} {randint(1,1147483647)}")
			self.main_thread = CommentThread()
			self.main_thread.save()
		super().save(*args,**kwargs)

class Comment(CommentThread):
	blogger = models.ForeignKey(User,on_delete=models.CASCADE)
	time_published = models.DateTimeField(default=timezone.now)
	expression = models.TextField()
	parent = models.ForeignKey(CommentThread,on_delete=models.CASCADE,related_name="+")
