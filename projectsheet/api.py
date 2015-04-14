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


class ProjectSheetTemplateResource(ModelResource):
    questions = fields.ToManyField(ProjectSheetQuestionResource, 'questions', full=True, null=True)

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


class ProjectSheetQuestionAnswerResource(ModelResource):
    question = fields.ToOneField(ProjectSheetQuestionResource, 'question', full=True)
    projectsheet = fields.ToOneField("projectsheet.api.ProjectSheetResource", 'projectsheet')

    class Meta:
        queryset = ProjectSheetQuestionAnswer.objects.all()
        allowed_methods = ['get', 'patch', 'post']
        resource_name = 'project/sheet/question_answer'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()


class ProjectSheetResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project', full=True)
    template = fields.ToOneField(ProjectSheetTemplateResource, 'template')
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True, full=True)
    cover = fields.ToOneField(BucketFileResource, 'cover', null=True, full=True)
    question_answers = fields.ToManyField(ProjectSheetQuestionAnswerResource, 'question_answers', null=True, full=True)
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
