from tastypie.resources import ModelResource
from tastypie import fields

from .models import Project, ProjectProgressRange, ProjectProgress

from scout.api import PostalAddressResource
from dataserver.authentication import AnonymousApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS

class ProjectProgressRangeResource(ModelResource):
    class Meta :
        queryset = ProjectProgressRange.objects.all()
        allowed_methods = ['get']
    
        filtering = {
            "slug": ('exact',),
        }
        
class ProjectProgressResource(ModelResource):
    range = fields.ToOneField(ProjectProgressRangeResource, "progress_range")
    
    class Meta:
        queryset = ProjectProgress.objects.all()
        allowed_methods = ['get']
        always_return_data = True
    
        filtering = {
            "range": ALL_WITH_RELATIONS,
        }
        

class ProjectResource(ModelResource):
    location = fields.ToOneField(PostalAddressResource, 'location', null=True, blank=True, full=True)
    progress = fields.ToOneField(ProjectProgressResource, 'progress', null=True, blank=True, full=True)
    
    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'project/project'
        always_return_data = True
        
        filtering = {
            "slug": ('exact',),
            'id' : ('exact', )
        }
        
        authorization = DjangoAuthorization()

    projecttool = fields.ForeignKey('projecttool.api.ProjectToolResource', 'projecttool', null=True, blank=True, full=True)
