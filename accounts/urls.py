from django.conf.urls import patterns, include

from tastypie.api import Api

from .api import ProfileResource, UserResource, ObjectProfileLinkResource

# REST API
account_api = Api(api_name='v0')

account_api.register(ProfileResource())
account_api.register(UserResource())
account_api.register(ObjectProfileLinkResource())

urlpatterns = patterns('',
    (r'^account/', include(account_api.urls)),
)
