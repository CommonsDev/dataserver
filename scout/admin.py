from django.contrib import admin

from .models import Map, TileLayer, Marker, MarkerCategory

class MapAdmin(admin.ModelAdmin):
    pass

class TileLayerAdmin(admin.ModelAdmin):
    pass

class MarkerAdmin(admin.ModelAdmin):
    pass

class MarkerCategoryAdmin(admin.ModelAdmin):
    pass

    
admin.site.register(Map, MapAdmin)
admin.site.register(TileLayer, TileLayerAdmin)
admin.site.register(Marker, MarkerAdmin)
admin.site.register(MarkerCategory, MarkerCategoryAdmin)