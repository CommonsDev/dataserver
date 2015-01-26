from django.contrib import admin
from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    model = Wallet

admin.site.register(Wallet, WalletAdmin)