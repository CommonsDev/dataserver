from tastypie.resources import ModelResource
from tastypie import fields

from .models import Room

class RoomResource(ModelResource):
    class Meta:
        queryset = Room.objects.all()

    bucket = fields.ToOneField('bucket.api.BucketResource', 'bucket', full=True)
    issue_tracker = fields.ToOneField('flipflop.api.BoardResource', 'issue_tracker', full=True)            

    def get_object_list(self, request):
        return super(RoomResource, self).get_object_list(request)
    
