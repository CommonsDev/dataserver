from django.conf.urls import *

from tastypie.resources import ModelResource
from tastypie import fields

from .models import Post

from graffiti.api import TaggedItemResource
from dataserver.authentication import AnonymousApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash

from accounts.api import ProfileResource


class PostResource(ModelResource):

    """ A post resource """

    author = fields.OneToOneField(ProfileResource, 'author', full=True)
    tags = fields.ToManyField(TaggedItemResource, 'tagged_items', full=True, null=True)

    class Meta:
        queryset = Post.objects.all()
        resource_name = 'megafon/post'
        allowed_methods = ['get']

        filtering = {
            "slug": ('exact',),
            "level" : ('exact', ),
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/questions%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_questions'), name="api_get_questions"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/answers%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_answers'), name="api_get_answers"),
        ]

    def dehydrate(self, bundle):
        bundle.data['answers_count'] = bundle.obj.get_descendant_count()
        return bundle

    def get_questions(self, request, **kwargs):
        kwargs['level'] = 0
        return self.get_list(request, **kwargs)


    def get_answers(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        question = self.get_object_list(request).get(id=kwargs['pk'])
        bundles = [self.full_dehydrate(self.build_bundle(obj=answer, request=request)) for answer in question.get_children()]
        return self.create_response(request, bundles)
