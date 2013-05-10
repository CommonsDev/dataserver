from tastypie.resources import ModelResource

from .models import Map, TileLayer

class MapResource(ModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'map'


class TileLayerResource(ModelResource):
    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'tilelayer'