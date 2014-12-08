from tastypie import fields
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from dataserver.authentication import AnonymousApiKeyAuthentication
from scout.api import PostalAddressResource, PlaceResource

from .models import Project, ProjectProgressRange, ProjectProgress

class ProjectResource(ModelResource):
    location = fields.ToOneField(PlaceResource, 'location', full=True, null=True, blank=True)

    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'project/project'
        authorization = Authorization()

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
        resource_name = 'project'
        always_return_data = True

        filtering = {
            "slug": ('exact',),
            'id' : ('exact', ),
            'location': ALL_WITH_RELATIONS,
        }

        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
