from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource
from tastypie import fields

from taggit.models import Tag

from accounts.api import UserResource

from .models import Board, List, Card, Task, CardComment

class ListResource(ModelResource):
    class Meta:
        queryset = List.objects.all()
        resource_name = 'flipflop/list'

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        

    cards = fields.ToManyField('flipflop.api.CardResource', 'cards', full=True)

class BoardResource(ModelResource):
    class Meta:
        queryset = Board.objects.all()
        resource_name = 'flipflop/board'

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        

    lists = fields.ToManyField('flipflop.api.ListResource', 'lists', use_in='detail', full=True)
    members = fields.ToManyField(UserResource, attribute='members', null=True, blank=True, full=True)
    
class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'flipflop/task'

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'flipflop/tag'        

class CardResource(ModelResource):
    class Meta:
        queryset = Card.objects.all()
        resource_name = 'flipflop/card'
        always_return_data = True
        authentication = ApiKeyAuthentication()        
        authorization = Authorization()
        

    tasks = fields.ToManyField('flipflop.api.TaskResource', 'tasks', blank=True, full=True)
    tags = fields.ToManyField(TagResource, 'tags', blank=True, full=True)
    assigned_to = fields.ToManyField(UserResource, 'assigned_to', blank=True, full=True)
    submitter = fields.ToOneField(UserResource, 'submitter', full=True)
    list = fields.ToOneField(ListResource, 'list')
    comments = fields.ToManyField('flipflop.api.CardCommentResource', 'comments', use_in='detail', full=True)    

    completion = fields.IntegerField(attribute='completion', readonly=True)
    comment_count = fields.IntegerField(attribute='comment_count', readonly=True)
    attachment_count = fields.IntegerField(attribute='attachment_count', readonly=True)


    def hydrate(self, bundle):
        if not bundle.obj.pk:
            bundle.data['submitter'] = bundle.request.user
            
        return bundle    

class CardCommentResource(ModelResource):
    class Meta:
        queryset = CardComment.objects.all()
        resource_name = 'flipflop/cardcomment'
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def hydrate(self, bundle):    
            if not bundle.obj.pk:
                bundle.data['user'] = bundle.request.user

            return bundle
        

    user = fields.ForeignKey(UserResource, 'user', full=True)
    card = fields.ForeignKey(CardResource, 'card')