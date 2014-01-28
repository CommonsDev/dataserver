import base64
import os
import mimetypes

from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from django.contrib.auth.models import User

from pygeocoder import Geocoder

from accounts.api import ProfileResource

from bucket.models import Bucket
from .models import Map, DataLayer, TileLayer, Marker, MarkerCategory

class MapResource(GeoModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'scout/map'
        authentication = ApiKeyAuthentication()        
        authorization = DjangoAuthorization()
        always_return_data = True        
        detail_uri_name = 'slug'        

    data_layers = fields.ToManyField('scout.api.DataLayerResource', 'datalayers', full=True, null=True)
    tile_layer = fields.ForeignKey('scout.api.TileLayerResource', 'tilelayer', full=True)
    bucket = fields.ForeignKey('bucket.api.BucketResource', 'bucket', null=True, full=True)

    def hydrate(self, bundle, request=None):    
            if not bundle.obj.pk:
                bucket = Bucket.objects.create()
                bundle.data['bucket'] = {'pk': bucket.pk}

            return bundle


class MarkerCategoryResource(ModelResource):
    class Meta:
        queryset = MarkerCategory.objects.all()
        resource_name = 'scout/marker_category'
        #authentication = ApiKeyAuthentication()        
        #authorization = DjangoAuthorization()
        authorization = Authorization()        
    

class TileLayerResource(GeoModelResource):
    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'scout/tilelayer'
        authorization = DjangoAuthorization()        

    maps = fields.ToManyField(MapResource, 'maps', null=True)

class DataLayerResource(ModelResource):
    class Meta:
        queryset = DataLayer.objects.all()
        resource_name = 'scout/datalayer'
        authorization = DjangoAuthorization()
        
    markers = fields.ToManyField('scout.api.MarkerResource', 'markers', null=True, full=True)
    map = fields.ToOneField('scout.api.MapResource', 'map')
    
class MarkerResource(GeoModelResource):
    class Meta:
        queryset = Marker.objects.all()
        resource_name = 'scout/marker'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
    
    data_layer = fields.ToOneField(DataLayerResource, 'datalayer')
    created_by = fields.ToOneField(ProfileResource, 'created_by', full=True)
    category = fields.ToOneField(MarkerCategoryResource, 'category', full=True)

    def hydrate(self, bundle, request=None):
        if not bundle.obj.pk:
            user = User.objects.get(pk=bundle.request.user.id)
            bundle.data['created_by'] = {'pk': user.get_profile().pk}

        # Resolve position
        position = bundle.data['position']['coordinates']
        geo_results = Geocoder.reverse_geocode(position[0], position[1])
        if len(geo_results) > 0:
            bundle.data['address'] = geo_results[0]
            
        return bundle
        
