from rest_framework import serializers
from .models import*


class clubownerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Admin_to_Coins_club_owner
        fields=['Coins_Club_Owner_Id','numcoin','created_date']



class CointraderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coins_club_owner_to_Coins_trader
        fields = ['to_trader','amount','created_date']




class Jockey_club_ownerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader_to_Jockey_club_owner
        fields = ['to_Jockey_club_owner','amount','created_date']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader_to_User
        fields = ['to_User','amount','created_date']


class Audio_JockeySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_to_Audio_Jockey
        fields = ['to_Audio_Jockey','amount','created_date']

from rest_framework import serializers
from .models import Gift

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = '__all__'


