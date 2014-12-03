from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Map, DataLayer, TileLayer, Marker, MarkerCategory, Place, PostalAddress

class InlineMarkerCategory(admin.TabularInline):
    model = MarkerCategory

class MapAdmin(GuardedModelAdmin):
    model = Map
    inlines = [
        InlineMarkerCategory,
    ]

class TileLayerAdmin(admin.ModelAdmin):
    pass

class DataLayerAdmin(admin.ModelAdmin):
    pass


class MarkerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Map, MapAdmin)
admin.site.register(TileLayer, TileLayerAdmin)
admin.site.register(DataLayer, DataLayerAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(PostalAddress)
admin.site.register(Place)
