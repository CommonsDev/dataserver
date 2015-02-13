import json
import datetime

from django.conf.urls import url
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http.response import HttpResponse
from django.utils.text import slugify

from django_comments import Comment
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.utils import dict_strip_unicode_keys, trailing_slash
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import http

from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource, UserResource
from accounts.models import Profile

class CommentResource(ModelResource):
    comment = fields.CharField(attribute='comment')
    user = fields.ToOneField(UserResource, 'user', full='true')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        filtering = {
            "comment": ALL_WITH_RELATIONS,
            "content_type": "exact",
            "object_pk": "exact"
        }
        allowed_methods = ['get', 'post']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        default_format = "application/json"

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_pk>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
                   ]

    def dispatch_list(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if 'content_type' in kwargs and 'object_pk' in kwargs and request.method=="POST":
            data = json.loads(request.body)
            commented_item, created = Comment.objects.get_or_create(comment=data['comment_text'],
                                            user=request.user,
                                            user_name=request.user.username,
                                            content_type=ContentType.objects.get(model=kwargs['content_type']),
                                            object_pk=kwargs['object_pk'],
                                            site_id=settings.SITE_ID,
                                            submit_date=datetime.datetime.now())
            bundle = self.build_bundle(obj=commented_item, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)

            return self.create_response(request,
                                        bundle,
                                        response_class=http.HttpCreated,
                                        location=self.get_resource_uri(bundle))

        return ModelResource.dispatch_list(self, request, **kwargs)
