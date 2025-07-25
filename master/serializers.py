from rest_framework import serializers
from master.models import *
from django.utils import timezone

from Coins_trader.models import Coins_trader
from Coins_club_owner.models import Coins_club_owner
from Jockey_club_owner.serializers import Jockey_club_owner
from Audio_Jockey.serializers import Audio_Jockey

class masterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = '__all__'


class masterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text',)

        



class FollowerSerializer(serializers.ModelSerializer):
    user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    following_user = masterSerializer()

    class Meta:
        model = Follow1
        fields = ('following_user', 'created_at')


class getfollowerSerializer(serializers.ModelSerializer):
    is_followed = serializers.BooleanField(default=False)

    class Meta:
        model = Common
        fields = ('id','Name', 'email', 'Gender', 'Dob', 'profile_picture', 'Introduction_voice', 'Introduction_text', 'is_followed')


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Common
        fields = ('id','Name','email','phone','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','coins',)

class UserSearchSerializer(serializers.ModelSerializer):
    is_following = serializers.BooleanField(read_only=True)
    class Meta:
        model = Common
        fields = ('id','Name','email','Gender','Dob','profile_picture','Introduction_voice','Introduction_text','is_following',)



class CoinTransferSerializer(serializers.Serializer):
    receiver_uid = serializers.CharField()
    # date = serializers.CharField()
    amount = serializers.IntegerField(min_value=0)

# class GiftTransactionhistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GiftTransactionhistory
#         fields = ['sender', 'receiver', 'amount', 'created_date']

class UserSpentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSpent_Time
        fields = ['time_duration','user_uid','created_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Explicitly set the timezone to 'Asia/Kolkata'
        created_date = instance.created_date.astimezone(timezone.get_fixed_timezone(330))  # 330 is the offset for 'Asia/Kolkata'
        representation['created_date'] = created_date.strftime('%Y-%m-%d %H:%M:%S')

        return representation
    

    
    

class AllCoinsTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_trader
        fields = ('id', 'Name', 'phone','profile_picture','uid',)



class AllCoinsTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coins_club_owner
        fields = ('id', 'Name', 'phone','profile_picture','uid',)


class AllCoinsTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio_Jockey
        fields = ('id', 'Name', 'phone','profile_picture','uid',)
        


class AllCoinsTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jockey_club_owner
        fields = ('id', 'Name', 'phone','profile_picture','uid',)

#####
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.Name')  
    user_id = serializers.IntegerField(source='user.id') 

    class Meta:
        model = Post
        fields = ['id', 'user_id', 'user_name', 'text', 'image', 'video', 'created_at']
        read_only_fields = ['created_at']
