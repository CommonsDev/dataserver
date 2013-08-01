from tastypie.resources import ModelResource
from tastypie import fields

from .models import Bucket, BucketFile

class BucketResource(ModelResource):
    class Meta:
        queryset = Bucket.objects.all()

    files = fields.ToManyField('bucket.api.BucketFileResource', 'files', full=True)
        
    def get_object_list(self, request):
        return super(BucketResource, self).get_object_list(request)


class BucketFileResource(ModelResource):
    class Meta:
        queryset = BucketFile.objects.all()

    def get_object_list(self, request):
        return super(BucketFileResource, self).get_object_list(request)
        
