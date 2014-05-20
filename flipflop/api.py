from django.conf.urls import url
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.authentication import ApiKeyAuthentication, Authentication
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.utils import trailing_slash

from guardian.shortcuts import assign_perm

from accounts.api import UserResource

from .models import Board, List, Card, Task, CardComment, Label

class ListResource(ModelResource):
    class Meta:
        queryset = List.objects.all()
        resource_name = 'flipflop/list'
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        

    board = fields.ForeignKey('flipflop.api.BoardResource', 'board')
    cards = fields.ToManyField('flipflop.api.CardResource', 'cards', full=True, null=True, blank=True)

class BoardResource(ModelResource):
    class Meta:
        queryset = Board.objects.all()
        resource_name = 'flipflop/board'
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        

    lists = fields.ToManyField('flipflop.api.ListResource', 'lists', use_in='detail', full=True, null=True, blank=True)
    members = fields.ToManyField(UserResource, attribute='members', null=True, blank=True, full=True, readonly=True)
    labels = fields.ToManyField('flipflop.api.LabelResource', 'labels', null=True, blank=True, full=True)

    def obj_create(self, bundle, **kwargs):
        bundle = super(BoardResource, self).obj_create(bundle, **kwargs)
        # Create default labels
        for i in range(1, 6): 
           bundle.obj.labels.create(label="Label %d" % i)

        # Give permission to creator
        assign_perm('flipflop.change_board', bundle.request.user, bundle.obj)
            
        return bundle
    
class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'flipflop/task'
        always_return_data = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    card = fields.ForeignKey('flipflop.api.CardResource', 'card')

class LabelResource(ModelResource):
    class Meta:
        queryset = Label.objects.all()
        resource_name = 'flipflop/label'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

class CardResource(ModelResource):
    class Meta:
        queryset = Card.objects.all()
        resource_name = 'flipflop/card'
        always_return_data = True
        authentication = ApiKeyAuthentication()        
        authorization = Authorization()
        

    tasks = fields.ToManyField('flipflop.api.TaskResource', 'tasks', blank=True, full=True)
    labels = fields.ToManyField(LabelResource, 'labels', blank=True, null=True, full=True)
    assignees = fields.ToManyField(UserResource, 'assigned_to', blank=True, full=True)
    submitter = fields.ToOneField(UserResource, 'submitter', full=True)
    list = fields.ToOneField(ListResource, 'list')
    comments = fields.ToManyField('flipflop.api.CardCommentResource', 'comments', use_in='detail', full=True, null=True, blank=True)    

    completion = fields.IntegerField(attribute='completion', readonly=True)
    comment_count = fields.IntegerField(attribute='comment_count', readonly=True)
    attachment_count = fields.IntegerField(attribute='attachment_count', readonly=True)
    tasks_done_count = fields.IntegerField(attribute='tasks_done_count', readonly=True)

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