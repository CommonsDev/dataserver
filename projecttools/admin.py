from django.contrib import admin

from .models import ProjectTools

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProjectTools, ProjectAdmin)