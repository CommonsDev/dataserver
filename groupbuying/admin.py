from django.contrib import admin

from .models import GroupBuy, GroupBuyItem

# Register your models here.
admin.site.register(GroupBuy)
admin.site.register(GroupBuyItem)