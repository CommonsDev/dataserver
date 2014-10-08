from django.contrib import admin

# Register your models here.

from .models import Usage, Pertinence

class UsageAdmin(admin.ModelAdmin):
    pass


class PertinenceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Usage, UsageAdmin)	
admin.site.register(Pertinence, PertinenceAdmin)	