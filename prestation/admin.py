from django.contrib import admin
from .models import Prestation, PrestationModule, SelectedModules

class PrestationAdmin(admin.ModelAdmin):
    model = Prestation

class PrestationModuleAdmin(admin.ModelAdmin):
    model = PrestationModule

class SelectedModulesAdmin(admin.ModelAdmin):
    pass

admin.site.register(SelectedModules, SelectedModulesAdmin)	
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(PrestationModule, PrestationModuleAdmin)