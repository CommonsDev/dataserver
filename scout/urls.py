from django.conf.urls import patterns, include

from tastypie.api import Api

from .api import MapResource, DataLayerResource, TileLayerResource, MarkerResource, MarkerCategoryResource

# REST API
api = Api(api_name='scout')
api.register(MapResource())
api.register(TileLayerResource())
api.register(DataLayerResource())
api.register(MarkerResource())
api.register(MarkerCategoryResource())

urlpatterns = patterns('',
    # (r'^scout/', include(scout_api.urls)),
)
