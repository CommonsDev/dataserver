from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from .models import Ingredient, EvaluationIngredient

class IngredientResource(ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'ingredient'
        authorization = Authorization()


class EvaluationIngredientResource(ModelResource):
    class Meta:
        queryset = EvaluationIngredient.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'evaluationingredient'
        authorization = Authorization()

