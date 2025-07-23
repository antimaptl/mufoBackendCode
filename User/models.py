

from django.db import models
import uuid
from django.utils.timezone import now
from Coins_club_owner.models import *
from Coins_trader.models import *
from Jockey_club_owner.models import *
from Audio_Jockey.models import *

class User(models.Model):
    Name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    Gender = models.CharField(max_length=20, default='')
    Dob = models.DateField(null=True, blank=True)
    profile_picture = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_voice = models.CharField(max_length=200, default='', blank=True, null=True)
    Introduction_text = models.CharField(max_length=500, default='')
    Invitation_Code = models.IntegerField(null=True, blank=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.CharField(max_length=50, null=True, blank=True)
    usertype = models.CharField(max_length=50, null=True, blank=True)
    token = models.CharField(max_length=300, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved= models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    coins = models.PositiveIntegerField(default=0) 
    def __str__(self):
        return str(self.Name)



class Follow(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.user.Name
    



class Social_media(models.Model):
    Google = models.CharField(max_length=100, blank=True, null=True, unique=True)
    Facebook = models.CharField(max_length=100, blank=True, null=True, unique=True)
    Snapchat = models.CharField(max_length=100, blank=True, null=True, unique=True)
    def __str__(self):
        return str(self.Google)




    
class Transaction(models.Model):
    payment_id = models.CharField(max_length=200, verbose_name="Payment ID")
    order_id = models.CharField(max_length=200, verbose_name="Order ID")
    signature = models.CharField(max_length=500, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.id)
    

# #task center
class room_join_claim_coins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)
    
class room_create_claim_coins(models.Model):
    user = models.ForeignKey(Audio_Jockey, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(max_length=100)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)


class claim_coins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user)
    

class Audiojockeyloigin(models.Model):
    user = models.ForeignKey(Audio_Jockey, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)


class Jockeyclubownerlogin(models.Model):
    user = models.ForeignKey(Jockey_club_owner, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)
    def __str__(self):
        return str(self.user)



class Coins_traderdaliylogin(models.Model):
    user = models.ForeignKey(Coins_trader, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user)
    
class Coinsclubownerdaliylogin(models.Model):
    user = models.ForeignKey(Coins_club_owner, on_delete=models.CASCADE)
    claim_coins = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user)
   


##################
from django.db import models

class Post5(models.Model):
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)  # Assuming `Common` is your user model
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.Name} on {self.created_at}"
    
class Gift(models.Model):
    name = models.CharField(max_length=100)
    coin = models.IntegerField()

class GiftTransaction(models.Model):
    sender = models.ForeignKey("User.User", related_name='sent_gifts', on_delete=models.CASCADE)
    receiver = models.ForeignKey("User.User", related_name='received_gifts', on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.Name} sent {self.gift.name} to {self.receiver.Name}"