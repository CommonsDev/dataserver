from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from commons.models.usage import Project, Usage, Pertinence

class PertinenceResource(ModelResource):
    class Meta:
        queryset = Pertinence.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/commons/pertinence'
        authorization = Authorization()

    project = fields.ForeignKey('projects.api.ProjectResource', 'project', use_in='detail', null=True, blank=True, full=True)
    usage = fields.ForeignKey('commons.api.usage.UsageResource', 'usage', use_in='detail', full=True, null=True, blank=True)


class UsageResource(ModelResource):
    class Meta:
        queryset = Usage.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/commons/usage'
        authorization = Authorization()

    project = fields.ToManyField('projects.api.ProjectResource', 'project', use_in='detail', null=True, blank=True, full=True)
