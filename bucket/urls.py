from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .api import BucketResource, BucketFileResource
from .views import UploadView

# REST API
bucket_api = Api(api_name='v0')
bucket_api.register(BucketResource())
bucket_api.register(BucketFileResource())

urlpatterns = patterns('',
    (r'^multiup/', include('multiuploader.urls')),
    url(r'^upload/', UploadView.as_view(), name='bucket-upload'),
    (r'^api/', include(bucket_api.urls))
)
