from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource

from .models import GUPProfile

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
    
class ProfileResource(ModelResource):
    class Meta:
        queryset = GUPProfile.objects.all()
        resource_name = 'profile'

    user = fields.ToOneField(UserResource, 'user', full=True, related_name='profile')



