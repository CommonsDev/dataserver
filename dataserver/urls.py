from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from tastypie.api import Api

from scout.api import (MapResource, TileLayerResource, DataLayerResource,
                       MarkerResource, MarkerCategoryResource, PostalAddressResource, PlaceResource)

from accounts.api import UserResource, GroupResource
from bucket.api import BucketResource, BucketFileResource, BucketTagResource, BucketFileCommentResource
from flipflop.api import BoardResource, ListResource, CardResource, TaskResource, LabelResource, CardCommentResource

from transport_vlille.api import VlilleResource
from projects.api import ProjectResource
from projectsheet.api import ProjectSheetResource, ProjectSheetTemplateResource, ProjectSheetSuggestedItemResource, ProjectSheetQuestionResource
from commons.api import UsageResource, PertinenceResource
from unisson.api import IngredientResource, EvaluationIngredientResource


admin.autodiscover()

# Build API
api = Api(api_name='v0')

# Scout
api.register(MapResource())
api.register(TileLayerResource())
api.register(MarkerResource())
api.register(DataLayerResource())
api.register(MarkerCategoryResource())
api.register(PostalAddressResource())
api.register(PlaceResource())


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

# Vlille
api.register(VlilleResource())

# Projects
api.register(ProjectResource())

# Project Sheets
api.register(ProjectSheetResource())
api.register(ProjectSheetTemplateResource())
api.register(ProjectSheetSuggestedItemResource())
api.register(ProjectSheetQuestionResource())

# Commons
api.register(UsageResource())
api.register(PertinenceResource())

# Unisson
api.register(IngredientResource())
api.register(EvaluationIngredientResource())


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
