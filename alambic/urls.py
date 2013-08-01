from django.conf.urls import patterns, include

from tastypie.api import Api

from .api import RoomResource

# REST API
alambic_api = Api(api_name='v0')
alambic_api.register(RoomResource())

urlpatterns = patterns('',
    (r'^alambic/', include(alambic_api.urls)),
)
