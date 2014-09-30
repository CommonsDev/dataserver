from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from .models import Project
from scout.api import PostalAddressResource

class ProjectResource(ModelResource):
    location = fields.ToOneField(PostalAddressResource, 'location', null=True, blank=True)
     
    class Meta:
        queryset = Project.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'project'
        authorization = Authorization()
        always_return_data = True
        
        filtering = {
            "slug": ('exact',),
            'id' : ('exact', )
        }