from django.contrib import admin
from django.contrib.admin.options import StackedInline
from simple_history.admin import SimpleHistoryAdmin
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetQuestion, ProjectSheetQuestionAnswer, QuestionChoice


# HEADS UP: currently not possible to inherit from
#           StackedInline with SimpleHistoryAdmin.
class ProjectSheetQuestionAnswerInline(StackedInline):
    model = ProjectSheetQuestionAnswer
    extra = 0
    min_num = 0
    can_delete = False


class QuestionChoiceInline(StackedInline):
    model = QuestionChoice
    min_num = 1
    extra = 1
    readonly_fields = ('value',)


class ProjectSheetQuestionInline(StackedInline):
    model = ProjectSheetQuestion.template.through
    extra = 0
    min_num = 1
    readonly_fields = ('get_choices', 'edit_questions_link', )

    def get_choices(self, obj):
        choices_string = ""
        try:
            question_object = ProjectSheetQuestion.objects.get(pk=obj.projectsheetquestion_id)
            for choice in question_object.choices.all():
                choices_string += choice.text+', '
            return choices_string
        except Exception as e:
            return choices_string

    def edit_questions_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  'projectsheetquestion'),  args=[instance.projectsheetquestion_id] )
        if instance.projectsheetquestion_id:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

    get_choices.short_description = 'Choix'


class ProjectSheetQuestionAdmin(admin.ModelAdmin):
    exclude = ('template', )
    inlines = [QuestionChoiceInline]
    list_display = [ 'id', '__unicode__']

    # FIXME : adapt to M2M
    def related_template(self, obj):
        return '%s'%(obj.template.name)
    related_template.short_description = 'Template'


class ProjectSheetTemplateAdmin(admin.ModelAdmin):
    # pass
   inlines = [ProjectSheetQuestionInline]


class ProjectSheetAdmin(SimpleHistoryAdmin):
    inlines = [ProjectSheetQuestionAnswerInline]


admin.site.register(ProjectSheet, ProjectSheetAdmin)
admin.site.register(ProjectSheetTemplate, ProjectSheetTemplateAdmin)
admin.site.register(ProjectSheetQuestion, ProjectSheetQuestionAdmin)
