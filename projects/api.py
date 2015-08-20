""" Project-related API resources. """

from tastypie.resources import ModelResource
from tastypie import fields

from .models import Project, ProjectProgressRange, ProjectProgress

from base.api import HistorizedModelResource
from graffiti.api import TaggedItemResource
from scout.api import PlaceResource
from tastypie.authentication import (
    MultiAuthentication, BasicAuthentication,
)
from dataserver.authorization import AdminOrDjangoAuthorization
from dataserver.authentication import AnonymousApiKeyAuthentication
from tastypie.constants import ALL_WITH_RELATIONS

# from accounts.api import ProfileResource


class ProjectProgressRangeResource(ModelResource):

    """ Project progress range API resource. """

    class Meta:
        queryset = ProjectProgressRange.objects.all()
        allowed_methods = ['get', 'post', ]
        resource_name = 'project/progressrange'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()


        filtering = {
            "slug": ('exact',),
            "name": ('exact',),
        }


class ProjectProgressResource(ModelResource):

    """ Project progress API resource. """

    range = fields.ToOneField(ProjectProgressRangeResource, "progress_range")

    class Meta:
        queryset = ProjectProgress.objects.all()
        allowed_methods = ['get', 'post', ]
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()
        resource_name = 'project/progress'

        always_return_data = True

        filtering = {
            "range": ALL_WITH_RELATIONS,
        }


class ProjectHistoryResource(ModelResource):

    """ Project History API resource. """

    class Meta:
        queryset = Project.history.all()
        filtering = {'id': ALL_WITH_RELATIONS}


class ProjectResource(HistorizedModelResource):

    """ Project API resource. """

    location = fields.ToOneField(PlaceResource, 'location',
                                 null=True, blank=True, full=True)
    progress = fields.ToOneField(ProjectProgressResource, 'progress',
                                 null=True, blank=True, full=True)
    tags = fields.ToManyField(TaggedItemResource, 'tagged_items',
                              full=True, null=True)

    related_projects = fields.ToManyField('ProjectResource',
                                          'related_projects',
                                          full=True, null=True)

    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        resource_name = 'project/project'
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()
        history_resource_class = ProjectHistoryResource
        filtering = {
            'slug': ('exact',),
            'id': ('exact', ),
            'location': ALL_WITH_RELATIONS,
        }
