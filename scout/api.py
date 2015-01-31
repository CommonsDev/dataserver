import base64
import os
import mimetypes

from pygeocoder import Geocoder

from tastypie import fields
from tastypie.authorization import Authorization, ReadOnlyAuthorization,\
    DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from dataserver.authorization import GuardianAuthorization
from dataserver.authentication import AnonymousApiKeyAuthentication

from accounts.api import UserResource
from bucket.models import Bucket

from .models import (Map, DataLayer, TileLayer, Marker,
                     MarkerCategory, PostalAddress, Place)

class MapAuthorization(GuardianAuthorization):
    def __init__(self):
        super(MapAuthorization, self).__init__(
            create_permission_code="add_map",
            view_permission_code="view_map",
            update_permission_code="change_map",
            delete_permission_code="delete_map"
        )

    def read_detail(self, object_list, bundle):
        for obj in object_list:
            if obj.privacy != 'GROUP_RW_OTHERS_RO':
                return super(MapAuthorization, self).read_detail(object_list, bundle)

        return True

class MapResource(GeoModelResource):
    class Meta:
        queryset = Map.objects.all()
        resource_name = 'scout/map'
        authentication = AnonymousApiKeyAuthentication()
        authorization = MapAuthorization()

        always_return_data = True
        detail_uri_name = 'slug'

    # created_by = fields.ToOneField('accounts.api.UserResource', 'created_by', readonly=True)
    data_layers = fields.ToManyField('scout.api.DataLayerResource', 'datalayers', full=True, null=True)
    tile_layer = fields.ForeignKey('scout.api.TileLayerResource', 'tilelayer', full=True)
    bucket = fields.ForeignKey('bucket.api.BucketResource', 'bucket', null=True, full=True)
    marker_categories = fields.ToManyField('scout.api.MarkerCategoryResource', 'marker_categories', null=True, full=True)

    def obj_create(self, bundle, **kwargs):
        bundle.obj = Map(bucket=Bucket.objects.create(created_by=bundle.request.user), created_by=bundle.request.user)
        bundle = self.full_hydrate(bundle)
        bundle.obj.save()

        return bundle


class MarkerCategoryResource(ModelResource):
    class Meta:
        queryset = MarkerCategory.objects.all()
        resource_name = 'scout/marker_category'

        authentication = AnonymousApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()


class TileLayerResource(GeoModelResource):
    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'scout/tilelayer'

        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization() # FIXME


    maps = fields.ToManyField(MapResource, 'maps', null=True)

class DataLayerResource(ModelResource):
    class Meta:
        queryset = DataLayer.objects.all()
        resource_name = 'scout/datalayer'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()

    markers = fields.ToManyField('scout.api.MarkerResource', 'markers', null=True, full=True)
    map = fields.ToOneField('scout.api.MapResource', 'map')

class MarkerResource(GeoModelResource):
    class Meta:
        queryset = Marker.objects.all()
        resource_name = 'scout/marker'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    data_layer = fields.ToOneField(DataLayerResource, 'datalayer')
    created_by = fields.ToOneField(UserResource, 'created_by', full=True)
    category = fields.ToOneField(MarkerCategoryResource, 'category', full=True)

    def hydrate(self, bundle, request=None):
        if not bundle.obj.pk:
            bundle.data['created_by'] = bundle.request.user

        # Resolve position
        position = bundle.data['position']['coordinates']
        geo_results = Geocoder.reverse_geocode(position[0], position[1])
        if len(geo_results) > 0:
            bundle.data['address'] = geo_results[0]

        return bundle

class PostalAddressResource(ModelResource):
    class Meta:
        queryset = PostalAddress.objects.all()
        resource_name = 'scout/postaladdress'
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()


class PlaceResource(GeoModelResource):
    class Meta:
        queryset = Place.objects.all()
        resource_name = 'scout/place'
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

        filtering = {
            "geo": ALL
        }
