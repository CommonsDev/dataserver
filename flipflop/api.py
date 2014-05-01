from tastypie.resources import ModelResource
from tastypie import fields

from taggit.models import Tag

from accounts.api import UserResource

from .models import Board, List, Card, Task

class ListResource(ModelResource):
    class Meta:
        queryset = List.objects.all()
        resource_name = 'flipflop/list'

    cards = fields.ToManyField('flipflop.api.CardResource', 'cards', full=True)

class BoardResource(ModelResource):
    class Meta:
        queryset = Board.objects.all()
        resource_name = 'flipflop/board'        

    lists = fields.ToManyField('flipflop.api.ListResource', 'lists', use_in='detail', full=True)
    
class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'flipflop/task'        


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'flipflop/tag'        

class CardResource(ModelResource):
    class Meta:
        queryset = Card.objects.all()
        resource_name = 'flipflop/card'        

    tasks = fields.ToManyField('flipflop.api.TaskResource', 'tasks', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)
    assigned_to = fields.ToManyField(UserResource, 'assigned_to')

    completion = fields.IntegerField(attribute='completion', readonly=True)
        
    #def get_object_list(self, request):
    #    return super(RoomResource, self).get_object_list(request)
    
