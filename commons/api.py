from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Project, Usage, Pertinence

class UsageResource(ModelResource):
    class Meta:
        queryset = Usage.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'project/commons/usage'
        authorization = Authorization()

class PertinenceResource(ModelResource):
    class Meta:
        queryset = Pertinence.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'project/commons/pertinence'
        authorization = Authorization()

    project = fields.ForeignKey('projects.api.ProjectResource', 'project', full=True)
    usage = fields.ForeignKey('commons.api.UsageResource', 'usage', full=True)
