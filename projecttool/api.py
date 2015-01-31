from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from dataserver.authentication import AnonymousApiKeyAuthentication

from .models import Project, ProjectTool, ToolCategory


class ToolCategoryResource(ModelResource):
    class Meta:
        queryset = ToolCategory.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/tool/category'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()


class ProjectToolResource(ModelResource):
    class Meta:
        queryset = ProjectTool.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/tool'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()

    category = fields.ToOneField(ToolCategoryResource, 'category', null=True, blank=True, full=True)
