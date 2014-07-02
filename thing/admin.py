from django.contrib import admin
from .models import Place, Thing, PeopleThing

# Register your models here.


class PlaceAdmin(admin.ModelAdmin):
    pass


class ThingAdmin(admin.ModelAdmin):
    pass

class PeopleThingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Place, PlaceAdmin)
admin.site.register(Thing, ThingAdmin)
admin.site.register(PeopleThing, PeopleThingAdmin)