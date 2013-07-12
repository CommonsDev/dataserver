from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gup.views.home', name='home'),
    # url(r'^gup/', include('gup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^accounts/', include('userena.urls')),
  
    (r'^api/', include('scout.urls')),
    (r'^api/', include('accounts.urls')),                       
                       
    url(r'^djangular/', include('djangular.urls')),                       
                       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
)

