from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Prestation, PrestationModule, SelectedModules


class PrestationModuleResource(ModelResource):
    class Meta:
        queryset = PrestationModule.objects.all()
        allowed_methods = ['get']
        resource_name = 'prestation/modules'
        authorization = Authorization()

class PrestationResource(ModelResource):
    class Meta:
        queryset = Prestation.objects.all()
        allowed_methods = ['get']
        resource_name = 'prestation/prestation'
        authorization = Authorization()

    modules = fields.ToManyField(PrestationModuleResource, 'module', null=True, blank=True, full=True)


class SelectedModulesResource(ModelResource):
    class Meta:
        queryset = SelectedModules.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

    prestation = fields.ToManyField(PrestationResource, 'modules', null=True, blank=True, full=True)
