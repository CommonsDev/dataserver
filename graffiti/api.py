from taggit.models import Tag, TaggedItem
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import dict_strip_unicode_keys, trailing_slash
from django.contrib.contenttypes.models import ContentType
from tastypie.constants import ALL_WITH_RELATIONS
from dataserver.authentication import AnonymousApiKeyAuthentication
from django.http.response import HttpResponse
from tastypie import http
from django.utils.text import slugify
import json

class TagResource(ModelResource):
    name = fields.CharField(attribute='name')
    slug = fields.CharField(attribute='slug')

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        filtering = {
            "name":"exact",
        }
        allowed_methods = ['get']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

class TaggedItemResource(ModelResource):
    tag = fields.ToOneField(TagResource, 'tag', full=True)

    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'taggeditem'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        default_format = "application/json"
        filtering = {
                "tag" : ALL_WITH_RELATIONS
        }
        always_return_data = True

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<object_type>\w+?)/(?P<object_id>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/(?P<object_type>\w+?)/(?P<object_id>\d+?)/similars%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('get_similars'),
               name="api_get_similars"),
        ]

    def get_similars(self, request, **kwargs):
        obj = ContentType.objects.get(model=kwargs.pop('object_type')).get_object_for_this_type(id=kwargs["object_id"])
        return HttpResponse(json.dumps([{'id' : o.id, 'type' : ContentType.objects.get_for_model(o).model} for o in obj.tags.similar_objects()]))

    def dispatch_list(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if 'object_type' in kwargs and 'object_id' in kwargs and request.method=="POST":
            data = json.loads(request.body)
            if 'tag' in data:
                tag_obj, created = Tag.objects.get_or_create(name=data['tag'], slug=slugify(data['tag']))
                tagged_item, created = TaggedItem.objects.get_or_create(tag=tag_obj,
                                                 content_type=ContentType.objects.get(model=kwargs['object_type']),
                                                 object_id=kwargs['object_id'])

                bundle = self.build_bundle(obj=tagged_item, request=request)
                bundle = self.full_dehydrate(bundle)
                bundle = self.alter_detail_data_to_serialize(request, bundle)

                return self.create_response(request,
                                            bundle,
                                            response_class=http.HttpCreated,
                                            location=self.get_resource_uri(bundle))

        return ModelResource.dispatch_list(self, request, **kwargs)
