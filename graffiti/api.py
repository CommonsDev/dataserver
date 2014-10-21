from taggit.models import Tag
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag' 
        filtering = {
            "name":"exact",
        }
        allowed_methods = ['get']
        authorization = Authorization()
        always_return_data = True 