from taggit.models import Tag, TaggedItem
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from django.conf.urls import url
from tastypie.utils.urls import trailing_slash
from django.contrib.contenttypes.models import ContentType
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication
from django.http.response import HttpResponse
import json

class ContentTypeResource(ModelResource):
    class Meta:
        queryset = ContentType.objects.all()
        resource_name = 'contenttype'
        allowed_methods = ['get']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        filtering = {
            "name":"exact",
        }
        allowed_methods = ['get']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = Authorization()

class TaggedItemResource(ModelResource):
    tag = fields.ToOneField(TagResource, 'tag')
    object_type = fields.CharField()
    authentication = AnonymousApiKeyAuthentication()
    authorization = DjangoAuthorization()

    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'taggeditem'
        authorization = Authorization()
        filtering = {
            "object_id":"exact",
            "tag" : ALL_WITH_RELATIONS
        }

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<object_type>\w+?)/(?P<object_id>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/(?P<object_type>\w+?)/(?P<object_id>\d+?)/similars%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('get_similars'),
               name="api_get_similars"),
            url(r"^(?P<resource_name>%s)/(?P<object_type>\w+?)/(?P<object_id>\d+?)/(?P<tag_id>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_detail'),
               name="api_dispatch_detail"),
        ]

    def get_similars(self, request, **kwargs):
        obj = ContentType.objects.get(model=kwargs.pop('object_type')).get_object_for_this_type(id=kwargs["object_id"])
        return HttpResponse(json.dumps([o.id for o in obj.tags.similar_objects()]))

    def dispatch_list(self, request, **kwargs):
        if 'object_type' in kwargs :
            kwargs["content_type"] = ContentType.objects.get(model=kwargs.pop('object_type'))
        if 'tag_id' in kwargs:
            kwargs["tag"] = Tag.objects.get(id=kwargs.pop('tag_id'))
        return ModelResource.dispatch_list(self, request, **kwargs)

    def dispatch_detail(self, request, **kwargs):
        if 'object_type' in kwargs :
            kwargs["content_type"] = ContentType.objects.get(model=kwargs.pop('object_type'))
        if 'tag_id' in kwargs:
            kwargs["tag"] = Tag.objects.get(id=kwargs.pop('tag_id'))
        return ModelResource.dispatch_detail(self, request, **kwargs)

    def dehydrate(self, bundle):
        bundle.data["object_type"] = "%s" % bundle.obj.content_type.model
        return bundle
