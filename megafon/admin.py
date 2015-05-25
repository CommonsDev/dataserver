from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post

admin.site.register(Post, MPTTModelAdmin)
