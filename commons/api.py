from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from .models import Project, Usage, Pertinence

class UsageResource(ModelResource):
    class Meta:
        queryset = Usage.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'usage'
        authorization = Authorization()


class PertinenceResource(ModelResource):
    class Meta:
        queryset = Pertinence.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'pertinence'
        authorization = Authorization()

