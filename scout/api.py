""" Scout API resources. """
# import base64
# import os
# import mimetypes

from pygeocoder import Geocoder

from tastypie import fields
from tastypie.constants import ALL
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
# from tastypie.fields import DictField
from tastypie.resources import ModelResource

from tastypie.authentication import (
    MultiAuthentication, BasicAuthentication,
)
from dataserver.authorization import (
    GuardianAuthorization, AdminOrDjangoAuthorization,
)
from dataserver.authentication import AnonymousApiKeyAuthentication

from accounts.api import UserResource
from bucket.models import Bucket

from .models import (Map, DataLayer, TileLayer, Marker,
                     MarkerCategory, PostalAddress, Place)


class MapAuthorization(GuardianAuthorization):

    """ Map Authorization. """

    def __init__(self):
        """ Howdy, pep257. """

        super(MapAuthorization, self).__init__(
            create_permission_code="add_map",
            view_permission_code="view_map",
            update_permission_code="change_map",
            delete_permission_code="delete_map"
        )

    def read_detail(self, object_list, bundle):
        """ Howdy, pep257. """

        for obj in object_list:
            if obj.privacy != 'GROUP_RW_OTHERS_RO':
                return super(MapAuthorization,
                             self).read_detail(object_list, bundle)

        return True


class MapResource(GeoModelResource):

    """ Map API resource. """

    class Meta:
        queryset = Map.objects.all()
        resource_name = 'scout/map'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = MapAuthorization()

        always_return_data = True
        detail_uri_name = 'slug'

    created_by = fields.ToOneField('accounts.api.UserResource', 'created_by',
                                   readonly=True)
    data_layers = fields.ToManyField('scout.api.DataLayerResource',
                                     'datalayers', full=True, null=True)
    tile_layer = fields.ForeignKey('scout.api.TileLayerResource', 'tilelayer',
                                   full=True)
    bucket = fields.ForeignKey('bucket.api.BucketResource', 'bucket',
                               null=True, full=True)
    marker_categories = fields.ToManyField('scout.api.MarkerCategoryResource',
                                           'marker_categories', null=True,
                                           full=True)

    def obj_create(self, bundle, **kwargs):
        """ Howdy, pep257. """

        bundle.obj = Map(bucket=Bucket.objects.create(
                         created_by=bundle.request.user),
                         created_by=bundle.request.user)
        bundle = self.full_hydrate(bundle)
        bundle.obj.save()

        return bundle


class MarkerCategoryResource(ModelResource):

    """ Marker category API resource. """

    class Meta:
        queryset = MarkerCategory.objects.all()
        resource_name = 'scout/marker_category'

        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()


class TileLayerResource(GeoModelResource):

    """ Tile layer API resource. """

    class Meta:
        queryset = TileLayer.objects.all()
        resource_name = 'scout/tilelayer'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()

    maps = fields.ToManyField(MapResource, 'maps', null=True)


class DataLayerResource(ModelResource):

    """ Data Layer API resource. """

    class Meta:
        queryset = DataLayer.objects.all()
        resource_name = 'scout/datalayer'

        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()

    markers = fields.ToManyField('scout.api.MarkerResource', 'markers',
                                 null=True, full=True)
    map = fields.ToOneField('scout.api.MapResource', 'map')
    json_mapping = fields.DictField(attribute='json_mapping')


class MarkerResource(GeoModelResource):

    """ Marker API resource. """

    class Meta:
        queryset = Marker.objects.all()
        resource_name = 'scout/marker'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()
        always_return_data = True

    data_layer = fields.ToOneField(DataLayerResource, 'datalayer')
    created_by = fields.ToOneField(UserResource, 'created_by', full=True)
    category = fields.ToOneField(MarkerCategoryResource, 'category', full=True)

    def hydrate(self, bundle, request=None):
        """ Hydrate address on the fly. """

        if not bundle.obj.pk:
            bundle.data['created_by'] = bundle.request.user

        # Resolve position
        position = bundle.data['position']['coordinates']
        geo_results = Geocoder.reverse_geocode(position[0], position[1])
        if len(geo_results) > 0:
            bundle.data['address'] = geo_results[0]

        return bundle


class PostalAddressResource(ModelResource):

    """ Postal address API resource. """

    class Meta:
        queryset = PostalAddress.objects.all()
        resource_name = 'scout/postaladdress'
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()


class PlaceResource(GeoModelResource):

    """ Place API resource. """

    class Meta:
        queryset = Place.objects.all()
        resource_name = 'scout/place'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()
        always_return_data = True

        filtering = {
            "geo": ALL,
        }
