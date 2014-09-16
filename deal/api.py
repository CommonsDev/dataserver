from django.conf.urls import url
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.utils import trailing_slash

from accounts.api import UserResource
from dataserver.authorization import GuardianAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from .models import Deal

class DealResource(ModelResource):
    class Meta:
        queryset = Deal.objects.all()
        resource_name = 'deal/deal'
        always_return_data = True
        filtering = {
            'ressource_uri': ALL
        }
        authentication = Authentication()
        authorization = Authorization()

    dealer = fields.ForeignKey(UserResource, 'dealer', full=True)
    members = fields.ToManyField(UserResource, 'members', full=True, null=True, blank=True)
