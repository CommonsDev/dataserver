""" Bucket-related API resources. """
import json

from django.contrib.auth.models import Group
from django.conf.urls import url
# from django.core.paginator import Paginator, InvalidPage
# from django.http import Http404
from django.shortcuts import get_object_or_404

from accounts.api import UserResource
from haystack.query import SearchQuerySet
from guardian.shortcuts import assign_perm
from taggit.models import Tag
from tastypie.authentication import (
    MultiAuthentication, BasicAuthentication,
)
from dataserver.authorization import (
    AdminOrDjangoAuthorization,
    GuardianAuthorization,
)
from dataserver.authentication import AnonymousApiKeyAuthentication

from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields

from .models import Bucket, BucketFile, BucketFileComment


class BucketResource(ModelResource):

    """ Bucket API resource. """

    class Meta:
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        # authorization = AdminOrDjangoAuthorization()
        authorization = GuardianAuthorization(
            create_permission_code="add_bucket",
            view_permission_code="view_bucket",
            update_permission_code="change_bucket",
            delete_permission_code="delete_bucket"
        )
        resource_name = 'bucket/bucket'
        always_return_data = True
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files',
                               full=True, null=True)

    def obj_create(self, bundle, **kwargs):
        """ Howdy, pep257. """

        bundle.obj = Bucket(created_by=bundle.request.user)
        bundle = self.full_hydrate(bundle)
        bundle.obj.save()

        return bundle

    def prepend_urls(self):
        """ URL override.

        For when a user wants to share a bucket with a group (assign a
        bucket to a group).
        """
        return [
            url(r"^(?P<resource_name>%s)/(?P<bucket_id>\d+)/assign%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('bucket_assign'), name="api_bucket_assign"),
        ]

    def bucket_assign(self, request, **kwargs):
        """ Assign edit permissions for a bucket to a group.

        The group is passed as POST parameter 'group_id'.
        """

        self.method_check(request, allowed=['post'])
        self.throttle_check(request)
        self.is_authenticated(request)

        target_group_id = json.loads(request.body)['group_id']
        target_group = get_object_or_404(Group, pk=target_group_id)
        bucket_id = kwargs['bucket_id']
        bucket = get_object_or_404(Bucket, pk=bucket_id)
        # assign bucket to group
        assign_perm("view_bucket", user_or_group=target_group, obj=bucket)
        assign_perm("change_bucket", user_or_group=target_group, obj=bucket)
        return self.create_response(request, {'success': True})


class BucketTagResource(ModelResource):

    """ Bucket tag API resource. """

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'bucket/tag'
        filtering = {
            "name": "exact",
        }
        allowed_methods = ['get', 'post', 'patch']
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()

    def hydrate(self, bundle, request=None):
        """ Hydrate dumb names to proper objects.

        We allow sending dumb tag objects with only a "name" attribute,
        then we retrieve or create proper tag objects
        """
        if bundle.data["name"]:
            tagName = bundle.data["name"]
            try:
                tag = Tag.objects.get(name=tagName)
            except Tag.DoesNotExist:
                tag = Tag(name=tagName)
                tag.save()
            bundle = self.build_bundle(obj=tag)
        return bundle


class BucketFileResource(ModelResource):

    """ Rest Resource for a given file of a given bucket. """

    class Meta:
        queryset = BucketFile.objects.all()
        resource_name = 'bucket/file'
        filtering = {
            "bucket": 'exact',
        }

        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()

    comments = fields.ToManyField('bucket.api.BucketFileCommentResource',
                                  'comments', full=True)
    tags = fields.ToManyField(BucketTagResource, 'tags', full=True)
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True)
    uploaded_by = fields.ToOneField(UserResource, 'uploaded_by', full=True)
    file = fields.FileField(attribute='file')
    filename = fields.CharField(attribute='filename', null=True)
    being_edited_by = fields.ToOneField(UserResource, 'being_edited_by',
                                        full=True, null=True)

    def hydrate(self, bundle, request=None):
        """ Hydrate users (uploaders) on the fly. """

        # Assign current user to new file
        if not bundle.obj.pk:
            bundle.data['uploaded_by'] = bundle.request.user

        return bundle

    def prepend_urls(self):
        """ Add search URL. """

        return [
            url(r"^(?P<resource_name>%s)/bucket/(?P<bucket_id>\d+)/search%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('file_search'), name="api_file_search"),
        ]

    def file_search(self, request, **kwargs):
        """ Implement file searching. """

        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        # URL params
        bucket_id = kwargs['bucket_id']
        # Query params
        query = request.GET.get('q', '')
        autocomplete = request.GET.get('auto', None)
        selected_facets = request.GET.getlist('facet', None)
        order = request.GET.getlist('order', '-pub_date')

        sqs = SearchQuerySet().models(BucketFile).filter(
            bucket=bucket_id).order_by(order).facet('tags')

        # 1st narrow down QS
        if selected_facets:
            for facet in selected_facets:
                sqs = sqs.narrow('tags:%s' % (facet))
        # A: if autocomplete, we return only a list of tags starting
        # with "auto" along with their count.
        if autocomplete is not None:
            tags = sqs.facet_counts()
            tags = tags['fields']['tags']
            if len(autocomplete) > 0:
                tags = [t for t in tags if t[0].startswith(autocomplete)]
            tags = [
                {'name': t[0], 'count':t[1]} for t in tags
            ]
            object_list = {
                'objects': tags,
            }

        # B: else, we return a list of files
        else:
            if query != "":
                sqs = sqs.auto_query(query)

            objects = []
            # Building object list
            for result in sqs:
                bundle = self.build_bundle(obj=result.object, request=request)
                bundle = self.full_dehydrate(bundle)
                objects.append(bundle)

            object_list = {
                'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class BucketFileCommentResource(ModelResource):

    """ File comment API resource. """

    class Meta:
        queryset = BucketFileComment.objects.all()
        always_return_data = True
        resource_name = 'bucket/filecomment'
        authentication = MultiAuthentication(BasicAuthentication(),
                                             AnonymousApiKeyAuthentication())
        authorization = AdminOrDjangoAuthorization()
        filtering = {
            "bucket_file": 'exact',
        }

    submitter = fields.ToOneField(UserResource, 'submitter', full=True)
    bucket_file = fields.ToOneField(BucketFileResource, 'bucket_file')

    def hydrate(self, bundle, request=None):
        """ Hydrate submitter as the request user on the fly. """

        if not bundle.obj.pk:
            bundle.data['submitter'] = bundle.request.user
        return bundle
