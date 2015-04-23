from django.contrib import admin
from django.contrib.admin.options import StackedInline
# from django import forms

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    ProjectSheet, ProjectSheetTemplate,
    ProjectSheetQuestion, ProjectSheetQuestionAnswer,
)


# HEADS UP: currently not possible to inherit from
#           StackedInline with SimpleHistoryAdmin.
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


class ProjectSheetAdmin(SimpleHistoryAdmin):
    inlines = [ProjectSheetQuestionAnswerInline]


admin.site.register(ProjectSheet, ProjectSheetAdmin)
admin.site.register(ProjectSheetTemplate, ProjectSheetTemplateAdmin)
