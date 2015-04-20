from django.contrib import admin

from .models import ToolCategory, ProjectTool


admin.site.register(ProjectTool)
admin.site.register(ToolCategory)