from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from accounts.api import UserResource

from .models import Map, TileLayer, Marker

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
    
    tile_layer = fields.ToOneField(TileLayerResource, 'tile_layer')
    created_by = fields.ToOneField(UserResource, 'created_by', full=True) 
    
    
    
    
    
    
        

        