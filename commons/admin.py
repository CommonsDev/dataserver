from django.contrib import admin
from commons.models.prestation import Prestation, PrestationModule, SelectedModules
from commons.models.usage import Project, Usage, Pertinence

class UsageAdmin(admin.ModelAdmin):
    pass

class PertinenceAdmin(admin.ModelAdmin):
    pass

class PrestationAdmin(admin.ModelAdmin):
    model = Prestation

class PrestationModuleAdmin(admin.ModelAdmin):
    model = PrestationModule

class SelectedModulesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usage, UsageAdmin)	
admin.site.register(Pertinence, PertinenceAdmin)	
admin.site.register(SelectedModules, SelectedModulesAdmin)	
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(PrestationModule, PrestationModuleAdmin)
