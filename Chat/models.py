from django.db import models
from User.models import User
from master.models import Common 
from Audio_Jockey.models import Audio_Jockey
import random, string , os 
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
class Bot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    file_name = models.CharField(max_length=33)
    message_handler = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.description or self.file_name
    
    def save(self, *args, **kwargs):
        dirname = os.path.dirname(self.file_name)
        if dirname:
            self.file_name = self.file_name.replace(dirname,'').replace('/','')
        return super().save(*args, **kwargs)

class Room(models.Model):
    ROOM_VISIBILITY = (
        (0, 'only user that know room code can join'),
        (1, 'Anyone can join, room will shown in chat index')
    )

    room_code = models.CharField(max_length=8)
    room_name = models.CharField(max_length=255)
    room_Image = models.CharField(max_length=500,blank=True)
    room_background_Image = models.CharField(max_length=500,blank=True)
    room_category = models.CharField(max_length=500,blank=True)
    is_public = models.IntegerField(choices=ROOM_VISIBILITY, default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_users_set',blank=True)
    active_bots = models.ManyToManyField(Bot,blank=True) 

    def save(self, room_code=True, *args, **kwargs):
        if not room_code:
            self.room_code = self.__generate_code()
        super().save(*args, **kwargs)
    
    def __repr__(self):
        return self.room_name
    
    def __str__(self):
        return self.room_name

    def __generate_code(self):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

class Visitor(models.Model):
    user_agent = models.TextField(null=True)
    ip_addr = models.GenericIPAddressField()

    def save(self, *args, **kwargs):
        if self.user_agent in settings.USER_AGENT_BLACKLIST:
            return None 
        return super().save(*args, **kwargs)

    def __repr__(self):
        return '<user_agent:{}'.format(self.user_agent)    

class Chat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True,blank=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __repr__(self):
        return '<from_user:{}'.format(self.from_user.username)


class ChatMessage(models.Model):
    sender = models.ForeignKey(Common, on_delete=models.CASCADE, related_name='sent_messages',blank=True,null=True)
    receiver = models.ForeignKey(Common, on_delete=models.CASCADE, related_name='received_messages',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()



class Notificationupdate(models.Model):
    user = models.ForeignKey(Common, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)+""+str(self.created_at)
    
    def save(self, user_group_name=None, *args, **kwargs):
        # print('saving notificationi')
        channel_layer = get_channel_layer()
        notification_objs = Notificationupdate.objects.filter(is_read=False).count()
        data = {'count': notification_objs, 'current_notification': self.message}
        print(f'saving notification:{self.message}')
        user_group_name = f"{self.user.uid}_group"
        async_to_sync(channel_layer.group_send)(
            user_group_name, {
                "type": "send_notification",
                "value": json.dumps(data)
            }
        )
        super(Notificationupdate, self).save(*args, **kwargs)