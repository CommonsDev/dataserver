from django.conf.urls import patterns, include

from tastypie.api import Api

from .api import MapResource, TileLayerResource, MarkerResource, MarkerCategoryResource

# REST API
scout_api = Api(api_name='v0')
scout_api.register(MapResource())
scout_api.register(TileLayerResource())
scout_api.register(MarkerResource())
scout_api.register(MarkerCategoryResource())

urlpatterns = patterns('',
    (r'^scout/', include(scout_api.urls)),
)
