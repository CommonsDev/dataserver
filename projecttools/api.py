from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import Project, ProjectTools
from tastypie import fields

class ProjectToolsResource(ModelResource):
    class Meta:
        queryset = ProjectTools.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'projecttools'
        authorization = Authorization()

    
  

