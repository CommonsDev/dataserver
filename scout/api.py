import base64
import os
import mimetypes

from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.resources import ModelResource

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.api import ProfileResource

from .models import Map, DataLayer, TileLayer, Marker, MarkerCategory

class Base64FileField(fields.FileField):
    """
    A django-tastypie field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    Usage:

    class MyResource(ModelResource):
        file_field = Base64FileField("file_field")

        class Meta:
            queryset = ModelWithFileField.objects.all()

    In the case of multipart for submission, it would also pass the filename.
    By using a raw post data stream, we have to pass the filename within our
    file_field structure:

    file_field = {
        "name": "myfile.png",
        "file": "longbas64encodedstring",
        "content_type": "image/png" # on hydrate optional
    }

    Your file_field will by dehydrated in the above format if the return64
    keyword argument is set to True on the field, otherwise it will simply
    return the URL.
    """

    def __init__(self, **kwargs):
        self.return64 = kwargs.pop('return64', False)
        super(Base64FileField, self).__init__(**kwargs)

    def dehydrate(self, bundle, **kwargs):
        if not self.return64:
            instance = getattr(bundle.obj, self.instance_name, None)
            try:
                url = getattr(instance, 'url', None)
            except ValueError:
                url = None
            return url
        else:
            if (not self.instance_name in bundle.data
                    and hasattr(bundle.obj, self.instance_name)):
                file_field = getattr(bundle.obj, self.instance_name)
                if file_field:
                    content_type, encoding = mimetypes.guess_type(
                        file_field.file.name)
                    b64 = open(
                        file_field.file.name, "rb").read().encode("base64")
                    ret = {"name": os.path.basename(file_field.file.name),
                           "file": b64,
                           "content-type": (content_type or
                                            "application/octet-stream")}
                    return ret
            return None

    def hydrate(self, obj):
        value = super(Base64FileField, self).hydrate(obj)
        if value and isinstance(value, dict):
            return SimpleUploadedFile(value["name"],
                                      base64.b64decode(value["file"]),
                                      value.get("content_type",
                                                "application/octet-stream"))
        elif isinstance(value, basestring):
            return value
        else:
            return None


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

class MarkerCategoryResource(ModelResource):
    class Meta:
        queryset = MarkerCategory.objects.all()
        resource_name = 'scout/marker_category'
        authentication = ApiKeyAuthentication()        
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

    picture = Base64FileField(attribute="picture", null=True, blank=True)

    def hydrate(self, bundle, request=None):
        if not bundle.obj.pk:
            user = User.objects.get(pk=bundle.request.user.id)
            bundle.data['created_by'] = {'pk': user.get_profile().pk}
            
        return bundle
        
