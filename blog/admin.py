from django.contrib import admin
from django.db import models
from .models import Blog
from tinymce.widgets import TinyMCE

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.TextField: {'widget': TinyMCE(attrs={'cols':80,'rows':40})},
	}

admin.site.register(Blog,BlogAdmin)