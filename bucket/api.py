from django.contrib.auth.models import User
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie import fields
from taggit.models import Tag
from accounts.api import ProfileResource
from haystack.query import SearchQuerySet

from .models import Bucket, BucketFile, BucketFileComment


class BucketResource(ModelResource):
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()        
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', full=True, null=True)
        
    def get_object_list(self, request):
        return super(BucketResource, self).get_object_list(request)


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        
    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', null=True)
        
class BucketFileResource(ModelResource):
    
    comments = fields.ToManyField('bucket.api.BucketFileCommentResource', 'comments', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)    
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True)
   
    class Meta:
        queryset = BucketFile.objects.all()
        resource_name = 'bucketfile'
        filtering = {
            "bucket":'exact', 
        }
        
    def get_object_list(self, request):
        return super(BucketFileResource, self).get_object_list(request)
        
    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/bucket/(?P<bucket_id>\d+)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('file_search'), name="api_file_search"),
        ]

    def file_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        bucket_id = kwargs['bucket_id'] 

        # FIXME : use haystack
        query = request.GET.get('q', '')
        sqs = SearchQuerySet().models(BucketFile).load_all().auto_query(query)
        #tags_qs = Tag.objects.filter(name__contains=request.GET.get('tags', '')) 
        #sqs = BucketFile.objects.filter(bucket=bucket_id).filter(description__icontains=request.GET.get('q', '')).filter(tags__in=tags_qs).distinct()
        
        print sqs
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
        
class BucketFileCommentResource(ModelResource):
    class Meta:
        queryset = BucketFileComment.objects.all()
        always_return_data = True
        # FIXME: deal with authentification and authorization
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        filtering = {
            "bucket_file":'exact', 
        }
        
    submitter = fields.ToOneField(ProfileResource, 'submitter', full=True)
    bucket_file = fields.ToOneField(BucketFileResource, 'bucket_file')
    
    def get_object_list(self, request):
        return super(BucketFileCommentResource, self).get_object_list(request)
    
    def hydrate(self, bundle, request=None):
        if not bundle.obj.pk:
            user = User.objects.get(pk=bundle.request.user.id)
            bundle.data['submitter'] = {'pk': user.get_profile().pk}
            
        return bundle


