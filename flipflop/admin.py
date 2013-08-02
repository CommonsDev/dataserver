from django.contrib import admin

from .models import Board, List, Card, Task

class InlineTask(admin.TabularInline):
    model = Task

class CardAdmin(admin.ModelAdmin):
    model = Card
    inlines = [
        InlineTask,
    ]

class InlineList(admin.TabularInline):
    model = List
    
class BoardAdmin(admin.ModelAdmin):
    model = Board
    inlines = [
        InlineList,
    ]

admin.site.register(Card, CardAdmin)
admin.site.register(Board, BoardAdmin)
