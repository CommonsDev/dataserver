from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetQuestion, ProjectSheetQuestionAnswer
from projects.api import ProjectResource
from projects.models import Project
from django.core.urlresolvers import reverse
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication
from bucket.api import BucketResource, BucketFileResource

class ProjectSheetTemplateResource(ModelResource):
    questions = fields.ToManyField("projectsheet.api.ProjectSheetQuestionResource", 'projectsheetquestion_set', full=True, null=True)

    class Meta:
        queryset = ProjectSheetTemplate.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/sheet/template'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'slug' : ('exact', )
        }

    def dehydrate(self, bundle):
        bundle.data["questions"] = []
        for question in bundle.obj.questions.all():
            bundle.data["questions"].append(question.text)
        return bundle

class ProjectSheetQuestionResource(ModelResource):
    class Meta:
        queryset = ProjectSheetQuestion.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'project/sheet/question'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

    def hydrate(self, bundle):
        bundle.obj.template = ProjectSheetTemplate.objects.get(id=bundle.data["template_id"])
        return bundle

class ProjectSheetQuestionAnswerResource(ModelResource):
    class Meta:
        queryset = ProjectSheetQuestionAnswer.objects.all()
        allowed_methods = ['get', 'patch']
        resource_name = 'project/sheet/question_answer'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()


class ProjectSheetResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    template = fields.ToOneField(ProjectSheetTemplateResource, 'template')
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True, full=True)
    cover = fields.ToOneField(BucketFileResource, 'cover', null=True, full=True)
    question_answers = fields.ToManyField(ProjectSheetQuestionAnswerResource, 'question_answers', null=True)
    videos = fields.DictField(attribute='videos', null=True)


    class Meta:
        queryset = ProjectSheet.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        default_format = "application/json"
        resource_name = 'project/sheet/projectsheet'

        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'project' : ALL_WITH_RELATIONS,
            'template' : ALL_WITH_RELATIONS,
        }

    def hydrate(self, bundle):
        if "project_id" in bundle.data: # XXX: ???
            bundle.obj.project = Project.objects.get(id=bundle.data["project_id"])
        if "template_id" in bundle.data:
            bundle.obj.template = ProjectSheetTemplate.objects.get(id=bundle.data["template_id"])
        return bundle
