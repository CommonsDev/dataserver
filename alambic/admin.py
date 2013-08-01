from django.contrib import admin

from .models import Room

class RoomAdmin(admin.ModelAdmin):
    model = Room

admin.site.register(Room, RoomAdmin)
