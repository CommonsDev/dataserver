from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource
from tastypie import fields

from taggit.models import Tag

from .models import Bucket, BucketFile, BucketFileComment

class BucketResource(ModelResource):
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()        
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', full=True, null=True)
        
    def get_object_list(self, request):
        return super(BucketResource, self).get_object_list(request)

class BucketFileCommentResource(ModelResource):
    class Meta:
        queryset = BucketFileComment.objects.all()


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        
class BucketFileResource(ModelResource):
    class Meta:
        queryset = BucketFile.objects.all()

    comments = fields.ToManyField(BucketFileCommentResource, 'comments', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)    
        
    def get_object_list(self, request):
        return super(BucketFileResource, self).get_object_list(request)
        
