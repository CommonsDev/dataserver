from tastypie.resources import ModelResource
from tastypie import fields

from taggit.models import Tag

from accounts.api import ProfileResource

from .models import Board, List, Card, Task

class ListResource(ModelResource):
    class Meta:
        queryset = List.objects.all()

    cards = fields.ToManyField('flipflop.api.CardResource', 'cards', full=True)

class BoardResource(ModelResource):
    class Meta:
        queryset = Board.objects.all()

    lists = fields.ToManyField('flipflop.api.ListResource', 'lists', full=True)
    
class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()

    done = fields.BooleanField('done', use_in='list')


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()

class CardResource(ModelResource):
    class Meta:
        queryset = Card.objects.all()

    tasks = fields.ToManyField('flipflop.api.TaskResource', 'tasks', full=True)
    tags = fields.ToManyField(TagResource, 'tags', full=True)
    assigned_to = fields.ToManyField(ProfileResource, 'assigned_to') # XXX This is wrong! userid!=profileid
    
        
    #def get_object_list(self, request):
    #    return super(RoomResource, self).get_object_list(request)
    
