from tastypie.resources import ModelResource
from tastypie import fields

from .models import Bucket, BucketFile, BucketFileComment
from taggit.models import Tag

class BucketResource(ModelResource):
    class Meta:
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', full=True)
        
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
        
