from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import Project, ProjectTool
from tastypie import fields

class ProjectToolResource(ModelResource):
    class Meta:
        queryset = ProjectTool.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'project/tool'
        authorization = Authorization()

    
  
  

