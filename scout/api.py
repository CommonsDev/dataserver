from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from .models import Map, TileLayer, Marker

from accounts.api import ProfileResource

class MapResource(GeoModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'map'

    tile_layers = fields.ToManyField('scout.api.TileLayerResource', 'tilelayers', full=True)


class TileLayerResource(GeoModelResource):
    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'tilelayer'

    maps = fields.ToManyField(MapResource, 'maps')
    markers = fields.ToManyField('scout.api.MarkerResource', 'markers', full=True)

class MarkerResource(GeoModelResource):
    class Meta:
        queryset = Marker.objects.all()
        resource_name = 'marker'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()
    
    tile_layer = fields.ToOneField(TileLayerResource, 'tile_layer')
    created_by = fields.ToOneField(ProfileResource, 'created_by', full=True)
        
    
    
    
    
    
    
        

        