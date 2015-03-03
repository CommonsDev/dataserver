from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Map, DataLayer, TileLayer, Marker, MarkerCategory, Place, PostalAddress

class InlineMarkerCategory(admin.TabularInline):
    model = MarkerCategory

class InlineDataLayerAdmin(admin.StackedInline):
    model = DataLayer
    extra = 1

class MapAdmin(GuardedModelAdmin):
    inlines = [
        InlineMarkerCategory,
        InlineDataLayerAdmin
    ]

class TileLayerAdmin(admin.ModelAdmin):
    pass

class MarkerAdmin(admin.ModelAdmin):
    pass

class MarkerCategoryAdmin(admin.ModelAdmin):
    pass

class PostalAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Map, MapAdmin)
admin.site.register(TileLayer, TileLayerAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(PostalAddress)
admin.site.register(Place)
