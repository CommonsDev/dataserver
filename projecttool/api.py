from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from dataserver.authentication import AnonymousApiKeyAuthentication

from .models import Project, ProjectTool

class ProjectToolResource(ModelResource):
    class Meta:
        queryset = ProjectTool.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'project/tool'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()
