from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Map, DataLayer, TileLayer, Marker, MarkerCategory, Place, PostalAddress

class MapAdmin(GuardedModelAdmin):
    pass

class TileLayerAdmin(admin.ModelAdmin):
    pass

class DataLayerAdmin(admin.ModelAdmin):
    pass


class MarkerAdmin(admin.ModelAdmin):
    pass

class MarkerCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Map, MapAdmin)
admin.site.register(TileLayer, TileLayerAdmin)
admin.site.register(DataLayer, DataLayerAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(MarkerCategory, MarkerCategoryAdmin)
admin.site.register(PostalAddress)
admin.site.register(Place)
