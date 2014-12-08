from django.contrib import admin
from django.contrib.admin.options import StackedInline

from .models import Project, ProjectProgress, ProjectProgressRange

class ProjectProgressInline(StackedInline):
    model = ProjectProgress
    extra = 0
    min_num = 2
    can_delete = False

class ProjectProgressRangeAdmin(admin.ModelAdmin):
    inlines = [ProjectProgressInline]

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectProgressRange, ProjectProgressRangeAdmin)
