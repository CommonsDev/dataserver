from django.contrib import admin
from django import forms

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetQuestion, ProjectSheetSuggestedItem
from django.contrib.admin.options import StackedInline


class ProjectSheetSuggestedItemInline(StackedInline):
    model = ProjectSheetSuggestedItem
    extra = 0
    min_num = 0
    can_delete = False

    
class ProjectSheetQuestionInline(StackedInline):
    model = ProjectSheetQuestion
    extra = 0
    min_num = 1


class ProjectSheetTemplateAdmin(admin.ModelAdmin):
    inlines = [ProjectSheetQuestionInline]


class ProjectSheetAdmin(admin.ModelAdmin):
    inlines = [ProjectSheetSuggestedItemInline]

admin.site.register(ProjectSheet, ProjectSheetAdmin)
admin.site.register(ProjectSheetTemplate, ProjectSheetTemplateAdmin)
admin.site.register(ProjectSheetQuestion, admin.ModelAdmin)