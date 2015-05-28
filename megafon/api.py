from django.conf.urls import *

from tastypie.resources import ModelResource
from tastypie import fields

from .models import Post
from accounts.models import Profile

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
        allowed_methods = ['get', 'post']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

        filtering = {
            "slug": ('exact',),
            "level" : ('exact', ),
            "answers_count" : ('exact', ),
        }
        ordering = ['updated_on', 'answers_count']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/questions%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_questions'), name="api_get_questions"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/answers%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_answers'), name="api_get_answers"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/contributors%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_contributors'), name="api_get_contributors"),
        ]

    def get_questions(self, request, **kwargs):
        kwargs['level'] = 0
        return self.get_list(request, **kwargs)


    def get_answers(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        post = self.get_object_list(request).get(id=kwargs['pk'])
        answers = post.get_children()
        bundles = []

        for obj in answers:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        return self.create_response(request, {'objects' : bundles})

    def get_contributors(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        question = self.get_object_list(request).get(id=kwargs['pk'])
        contributors = question.get_descendants(include_self=False).values_list('author', flat=True)
        bundles = []

        for obj in Profile.objects.filter(id__in=contributors):
            contributor_resource = ProfileResource()
            bundle = contributor_resource.build_bundle(obj=obj, request=request)
            bundles.append(contributor_resource.full_dehydrate(bundle, for_list=True))

        return self.create_response(request, {'objects' : bundles})

    # def get_best_contributors(self, request, **kwargs):
        # Profile.objects.filter(id__gt=1).annotate(num_post=Count('post')).order_by('-num_post')