from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from scout.api import MapResource, TileLayerResource, DataLayerResource, MarkerResource, MarkerCategoryResource
from accounts.api import UserResource, GroupResource
from bucket.api import BucketResource, BucketFileResource, BucketTagResource, BucketFileCommentResource
from flipflop.api import BoardResource, ListResource, CardResource, TaskResource, LabelResource, CardCommentResource

import views

admin.autodiscover()

# Build API
api = Api(api_name='v0')

# Scout
api.register(MapResource())
api.register(TileLayerResource())
api.register(MarkerResource())
api.register(DataLayerResource())
api.register(MarkerCategoryResource())

# Auth
api.register(UserResource())
api.register(GroupResource())

# Kanban
api.register(BoardResource())
api.register(ListResource())
api.register(CardResource())
api.register(TaskResource())
api.register(CardCommentResource())
api.register(LabelResource())

# Bucket
api.register(BucketResource())
api.register(BucketTagResource())
api.register(BucketFileResource())
api.register(BucketFileCommentResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gup.views.home', name='home'),
    # url(r'^gup/', include('gup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^accounts/', include('userena.urls')),
  
    (r'^api/', include(api.urls)),
    (r'^api/', include('alambic.urls')),
    (r'^flipflop/', include('flipflop.urls')),
                       
    url(r'^djangular/', include('djangular.urls')),

    (r'^bucket/', include('bucket.urls')),

#    url(r'^select2/', include('django_select2.urls')),
                       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#CMS
urlpatterns += patterns('',
    url(r'^mapage/$', views.CMSRedirectView.as_view(), name='cmsredirect'),
    url(r'^', include('cms.urls')),
)

