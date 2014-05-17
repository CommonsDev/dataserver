from tastypie.resources import ModelResource
from tastypie import fields

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from .models import GroupBuy, GroupBuyItem

class GroupBuyItemResource(ModelResource):
    class Meta:
        queryset = GroupBuyItem.objects.all()
        

class GroupBuyResource(ModelResource):
    class Meta:
        queryset = GroupBuy.objects.all()
        resource_name = 'groupbuying/groupbuy'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True

    items = fields.ToManyField(GroupBuyItemResource, 'items', full=True, full_list=False, full_detail=True, blank=True)
    