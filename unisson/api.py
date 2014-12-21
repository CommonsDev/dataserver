from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Ingredient, EvaluationIngredient

class IngredientResource(ModelResource):
    class Meta:
        queryset = Ingredient.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'unisson/ingredient'
        authorization = Authorization()


class EvaluationIngredientResource(ModelResource):
    class Meta:
        queryset = EvaluationIngredient.objects.all()
        allowed_methods = ['get', 'post', 'patch']
        resource_name = 'unisson/evaluationingredient'
        authorization = Authorization()
    
    ingredient = fields.ToOneField(IngredientResource, 'ingredient', null=True, blank=True, full=True)
