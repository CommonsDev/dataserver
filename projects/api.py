from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, Authorization

from .models import Project

class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'project'
        authorization = Authorization()