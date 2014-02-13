from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .api import BucketResource, BucketFileResource, BucketFileCommentResource
from .views import UploadView, ThumbnailView


# REST API
bucket_api = Api(api_name='v0')
bucket_api.register(BucketResource())
bucket_api.register(BucketFileResource())
bucket_api.register(BucketFileCommentResource())

urlpatterns = patterns('',
    (r'^multiup/', include('multiuploader.urls')),
    url(r'^upload/', UploadView.as_view(), name='bucket-upload'),
    url(r'^(?P<pk>\d+)/thumbnail/', ThumbnailView.as_view(), name='bucket-thumbnail'),                       
    (r'^api/', include(bucket_api.urls))
)
