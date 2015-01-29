from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetSuggestedItem, ProjectSheetQuestion
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
        resource_name = 'projectsheettemplate'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'slug' : ('exact', )
        }

class ProjectSheetQuestionResource(ModelResource):
    class Meta:
        queryset = ProjectSheetQuestion.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'projectsheetquestion'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

class ProjectSheetSuggestedItemResource(ModelResource):
    question = fields.ToOneField(ProjectSheetQuestionResource, 'question', full=True)
    projectsheet = fields.ToOneField("projectsheet.api.ProjectSheetResource", 'projectsheet')

    class Meta:
        queryset = ProjectSheetSuggestedItem.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'projectsheetsuggesteditem'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

class ProjectSheetResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    template = fields.ToOneField(ProjectSheetTemplateResource, 'template', full=True)
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True, full=True)
    cover = fields.ToOneField(BucketFileResource, 'cover', null=True, full=True)
    videos = fields.DictField(attribute='videos', null=True)

    items = fields.ToManyField(ProjectSheetSuggestedItemResource, 'projectsheetsuggesteditem_set', null=True, full=True)

    class Meta:
        queryset = ProjectSheet.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        default_format = "application/json"
        resource_name = 'projectsheet'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'project' : ALL_WITH_RELATIONS,
            'template' : ALL_WITH_RELATIONS,
        }
