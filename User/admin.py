from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Social_media)
admin.site.register(claim_coins)
admin.site.register(room_join_claim_coins)
admin.site.register(Coinsclubownerdaliylogin)
admin.site.register(Coins_traderdaliylogin)
admin.site.register(Jockeyclubownerlogin)
admin.site.register(Audiojockeyloigin)
admin.site.register(room_create_claim_coins)
admin.site.register(Transaction)
#
# admin.py

from .models import User, Gift, GiftTransaction

admin.site.register(Gift)
# admin.site.register(User)
admin.site.register(GiftTransaction)




