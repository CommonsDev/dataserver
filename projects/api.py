from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from scout.api import PlaceResource

from .models import Project

class ProjectResource(ModelResource):
    location = fields.ToOneField(PlaceResource, 'location', full=True, null=True, blank=True)

    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'project/project'
        authorization = Authorization()
        always_return_data = True

        filtering = {
            "slug": ('exact',),
            'id' : ('exact', ),
            'location': ALL_WITH_RELATIONS,
        }
