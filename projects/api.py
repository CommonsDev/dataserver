from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from .models import Project

class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'project'
        authorization = Authorization()
        always_return_data = True
        
        filtering = {
            "slug": ('exact',),
        }