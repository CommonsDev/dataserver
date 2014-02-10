from django.contrib.auth.models import User

from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource
from tastypie import fields
from taggit.models import Tag
from accounts.api import ProfileResource

from .models import Bucket, BucketFile, BucketFileComment


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
        
class BucketFileResource(ModelResource):
    class Meta:
        queryset = BucketFile.objects.all()

    comments = fields.ToManyField('bucket.api.BucketFileCommentResource', 'comments', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)    
        
    def get_object_list(self, request):
        return super(BucketFileResource, self).get_object_list(request)
        
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
