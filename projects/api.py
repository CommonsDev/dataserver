from tastypie.resources import ModelResource
from tastypie import fields

from .models import Project

from scout.api import PostalAddressResource
from dataserver.authentication import AnonymousApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

class ProjectResource(ModelResource):
    location = fields.ToOneField(PostalAddressResource, 'location', null=True, blank=True)
     
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