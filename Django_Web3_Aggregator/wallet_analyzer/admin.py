from django.contrib import admin

# Register your models here.
from wallet_analyzer.models import Wallet
#
# @admin.register(Wallet) #delete
# class WalletAdmin(admin.ModelAdmin):
#     list_display = ('id', "address")
#     list_display_links = ('id', "address")