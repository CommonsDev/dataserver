from django.contrib import admin

from .models import ToolCategory, ProjectTools


admin.site.register(ProjectTools)
admin.site.register(ToolCategory)