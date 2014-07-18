from django.contrib import admin
from .models import Ingredient, EvaluationIngredient 

class EvaluationIngredientAdmin(admin.ModelAdmin):
    model = EvaluationIngredient
    list_filter = ['ingredient', 'project__title']
    search_fields = ['project__title']


admin.site.register(Ingredient)
admin.site.register(EvaluationIngredient, EvaluationIngredientAdmin)