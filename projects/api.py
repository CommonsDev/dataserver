from tastypie.resources import ModelResource
from tastypie import fields

from .models import Project, ProjectProgressRange, ProjectProgress, ProjectTeam

from scout.api import PostalAddressResource
from dataserver.authentication import AnonymousApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from accounts.api import ProfileResource

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
    team = fields.ToManyField("projects.api.ProjectTeamResource", "projectteam_set", full=True)
    
    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'project'
        always_return_data = True
        
        filtering = {
            "slug": ('exact',),
            'id' : ('exact', )
        }
        
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()


class ProjectTeamResource(ModelResource):
    project = fields.ToOneField(ProjectResource, "project")
    members = fields.ToManyField(ProfileResource, "members", full=True)
    
    class Meta:
        queryset = ProjectTeam.objects.all()
        allowed_methods = ['get',]
        always_return_data = True
    
        filtering = {
            "project": ALL_WITH_RELATIONS,
        }