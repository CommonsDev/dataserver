from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource

from .models import GUPProfile

class ProfileResource(ModelResource):
    class Meta:
        queryset = GUPProfile.objects.all()
        resource_name = 'profile'

        fields = ['mugshot']

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.user.username
        bundle.data['first_name'] = bundle.obj.user.first_name
        bundle.data['last_name'] = bundle.obj.user.last_name
        return bundle



