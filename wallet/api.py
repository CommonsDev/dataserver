from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from .models import Wallet

class WalletResource(ModelResource):
    class Meta:
        queryset = Wallet.objects.all()
        allowed_methods = ['get']
        resource_name = 'wallet'
        authorization = Authorization()

   