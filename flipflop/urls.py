from django.conf.urls import patterns, include, url

from tastypie.api import Api

from .api import BoardResource, CardResource, ListResource

# REST API
flipflop_api = Api(api_name='v0')
flipflop_api.register(BoardResource())
flipflop_api.register(CardResource())
flipflop_api.register(ListResource())

urlpatterns = patterns('',
    (r'^api/', include(flipflop_api.urls))
)
