from django.contrib.auth.models import User
from django.conf.urls import patterns, url, include
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
        authentication = Authentication()
        authorization = Authorization()        

        #authentication = ApiKeyAuthentication()
        #authorization = DjangoAuthorization()        
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', full=True, null=True)
        
    def get_object_list(self, request):
        return super(BucketResource, self).get_object_list(request)


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag' 
        filtering = {
            "name":"exact",
        }
        allowed_methods = ['get', 'post', 'patch']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()  
    
    def get_object_list(self, request):
        return super(TagResource, self).get_object_list(request)

    def hydrate(self, bundle, request=None):
        """
        We allow sending dumb tag objects with only a "name" attribute, then we retrieve or create proper tag objects
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
    """
    Rest Resource for a given file of a given bucket
    """
    class Meta:
        queryset = BucketFile.objects.all()
        resource_name = 'bucketfile'
        filtering = {
            "bucket":'exact', 
        }
        allowed_methods = ['get', 'post', 'patch', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()        
    
    comments = fields.ToManyField('bucket.api.BucketFileCommentResource', 'comments', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)    
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True)
    uploaded_by = fields.ToOneField(ProfileResource, 'uploaded_by', full=True)
    file = fields.FileField(attribute='file')
    filename = fields.CharField(attribute='filename', null=True)
    being_edited_by = fields.ToOneField(ProfileResource, 'being_edited_by', full=True, null = True)
    
    def hydrate(self, bundle, request=None):
        # Assign current user to new file
        if not bundle.obj.pk:
            user = User.objects.get(pk=bundle.request.user.id)
            bundle.data['uploaded_by'] = {'pk': user.get_profile().pk}
        
        return bundle
        
    def get_object_list(self, request):
        return super(BucketFileResource, self).get_object_list(request)
        
    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/bucket/(?P<bucket_id>\d+)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('file_search'), name="api_file_search"),
        ]
    
    def file_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        # URL params
        bucket_id = kwargs['bucket_id'] 
        # Query params
        query = request.GET.get('q', '')
        autocomplete = request.GET.get('auto', None)
        selected_facets = request.GET.getlist('facet', None)
        order = request.GET.getlist('order', '-pub_date')
        
        sqs = SearchQuerySet().models(BucketFile).filter(bucket=bucket_id).order_by(order).facet('tags')
        
        # 1st narrow down QS
        if selected_facets:
            for facet in selected_facets:
                sqs = sqs.narrow('tags:%s' % (facet))
        # A: if autocomplete, we return only a list of tags starting with "auto" along with their count
        if autocomplete != None:
            tags = sqs.facet_counts()
            tags = tags['fields']['tags']
            if len(autocomplete) > 0:
                tags = [ t for t in tags if t[0].startswith(autocomplete) ]
            tags = [ {'name':t[0], 'count':t[1]} for t in tags ]
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


