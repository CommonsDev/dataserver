from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetSuggestedItem, ProjectSheetQuestion
from projects.api import ProjectResource
from projects.models import Project
from django.core.urlresolvers import reverse
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication


class ProjectSheetTemplateResource(ModelResource):
    class Meta:
        queryset = ProjectSheetTemplate.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/sheet/template'
        authorization = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'slug' : ('exact', )
        }

    def dehydrate(self, bundle):
        bundle.data["questions"] = []
        for question in bundle.obj.projectsheetquestion_set.all():
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

class ProjectSheetSuggestedItemResource(ModelResource):
    class Meta:
        queryset = ProjectSheetSuggestedItem.objects.all()
        allowed_methods = ['get', 'patch']
        resource_name = 'project/sheet/suggesteditem'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()


class ProjectSheetResource(ModelResource):
    project = fields.ToOneField(ProjectResource, 'project')
    template = fields.ToOneField(ProjectSheetTemplateResource, 'template')

    class Meta:
        queryset = ProjectSheet.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'project/sheet/projectsheet'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'project' : ALL_WITH_RELATIONS,
            'template' : ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data["items"] = []
        for item in bundle.obj.projectsheetsuggesteditem_set.all().order_by("question__order"):
            bundle.data["items"].append(reverse('api_dispatch_detail', kwargs={'api_name' : 'v0', #FIXME : hardcoded
                                                                 'resource_name' : 'project/sheet/suggesteditem',
                                                                 'pk' :item.id}))
        return bundle

    def hydrate(self, bundle):
        if "project_id" in bundle.data:
            bundle.obj.project = Project.objects.get(id=bundle.data["project_id"])
        if "template_id" in bundle.data:
            bundle.obj.template = ProjectSheetTemplate.objects.get(id=bundle.data["template_id"])
        return bundle
