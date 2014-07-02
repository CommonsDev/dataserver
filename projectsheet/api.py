from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from .models import ProjectSheet

class ProjectSheetResource(ModelResource):
    class Meta:
        queryset = ProjectSheet.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'projectsheet'
        authorization = Authorization()