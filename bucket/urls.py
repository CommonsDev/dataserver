from django.conf.urls import patterns, include, url

from .views import UploadView, ThumbnailView

urlpatterns = patterns('',
    (r'^multiup/', include('multiuploader.urls')),
    url(r'^upload/', UploadView.as_view(), name='bucket-upload'),
    url(r'^file/(?P<pk>\d+)/thumbnail/', ThumbnailView.as_view(), name='bucket-thumbnail'),        
)
