from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import Project, ToolCategory, ProjectTools
from tastypie import fields

class ToolCategoryResource(ModelResource):
    class Meta:
        queryset = ToolCategory.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'toolcategory'
        authorization = Authorization()

class ProjectToolsResource(ModelResource):
    class Meta:
        queryset = ProjectTools.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'projecttools'
        authorization = Authorization()

    
  
  

