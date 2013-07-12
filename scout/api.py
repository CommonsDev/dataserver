from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from django.contrib.auth.models import User

from .models import Map, TileLayer, Marker

from accounts.api import ProfileResource

class MapResource(GeoModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'map'
        authorization = DjangoAuthorization()
        detail_uri_name = 'slug'        

    tile_layers = fields.ToManyField('scout.api.TileLayerResource', 'tilelayers', full=True)


class TileLayerResource(GeoModelResource):
    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'tilelayer'
        authorization = DjangoAuthorization()        

    maps = fields.ToManyField(MapResource, 'maps')
    markers = fields.ToManyField('scout.api.MarkerResource', 'markers', full=True)

class MarkerResource(GeoModelResource):
    class Meta:
        queryset = Marker.objects.all()
        resource_name = 'marker'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
    
    tile_layer = fields.ToOneField(TileLayerResource, 'tile_layer')
    created_by = fields.ToOneField(ProfileResource, 'created_by', full=True)

    def hydrate(self, bundle, request=None):
        if not bundle.obj.pk:
            user = User.objects.get(pk=bundle.request.user.id)
            bundle.data['created_by'] = {'pk': user.get_profile().pk}
            
        return bundle     
        
    
    
    
    
    
    
        

        