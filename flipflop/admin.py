from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from .models import Board, List, Card, Task, CardComment

class InlineTask(admin.TabularInline):
    model = Task

class CardAdmin(admin.ModelAdmin):
    model = Card
    inlines = [
        InlineTask,
    ]

class InlineList(admin.TabularInline):
    model = List
    
class BoardAdmin(GuardedModelAdmin):
    model = Board
    inlines = [
        InlineList,
    ]

admin.site.register(Card, CardAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(CardComment)
