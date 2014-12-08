from django.contrib import admin
from django.contrib.admin.options import StackedInline
from django import forms

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetQuestion, ProjectSheetQuestionAnswer

class ProjectSheetQuestionAnswerInline(StackedInline):
    model = ProjectSheetQuestionAnswer
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
    inlines = [ProjectSheetQuestionAnswerInline]

admin.site.register(ProjectSheet, ProjectSheetAdmin)
admin.site.register(ProjectSheetTemplate, ProjectSheetTemplateAdmin)
