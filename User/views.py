
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from Mufo.Minxins import *
from .serializers import *
from .razorpay import RazorpayClient
rz_client = RazorpayClient()
from django.conf import settings
import json

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, response
import random
from django.utils import timezone
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta
from .models import User
from Audio_Jockey.models import Audio_Jockey
from coin.models import Purchase_history
from Coins_club_owner.models import Coins_club_owner
from Coins_trader.models import Coins_trader
from Jockey_club_owner.models import Jockey_club_owner
import secrets
from django.utils.decorators import method_decorator
from Mufo.Minxins import authenticate_token
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework import filters
from master.serializers import *
from master.models import *
from Chat.models import *
import uuid
from datetime import datetime

def Users(request):
    return HttpResponse("Hello, world. You're at the User index.")
    
class Register(APIView):
    serializer_class = UserSerializer
    serializer_class1 = masterSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @method_decorator(authenticate_token)
    def post(self, request):
        uid = request.user.uid  # Already authenticated via token
        user = get_object_or_404(User, uid=uid)
        try:
            common_obj = Common.objects.get(uid=uid)
        except Common.DoesNotExist:
            common_obj = None

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if common_obj:
            serializer1 = self.serializer_class1(common_obj, data=request.data, partial=True)
        else:
            serializer1 = self.serializer_class1(data=request.data)

        if serializer.is_valid():
            serializer.save()

            if serializer1.is_valid():
                serializer1.save(token=user.token, uid=uid, usertype=user.usertype, Is_Approved=True)
                return Response({
                    'data': serializer.data,
                    'access': user.token,
                    'message': "User data updated successfully"
                }, status=status.HTTP_200_OK)

            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class Login(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         phone = serializer.initial_data.get('phone')

#         profiles = [Audio_Jockey, Coins_club_owner,
#                     Coins_trader, Jockey_club_owner, User]
#         profile = None

#         for profile_model in profiles:
#             profile = profile_model.objects.filter(phone=phone).first()
#             if profile:
#                 break

#         if not profile:
#             return Response({'message': "No user found with this mobile"}, status=status.HTTP_404_NOT_FOUND)

#         if hasattr(profile, 'Is_Approved') and not profile.Is_Approved:
#             return Response({'message': f"{profile.__class__.__name__} {profile} is not approved Yet. Please wait for some time to get approved."}, status=status.HTTP_403_FORBIDDEN)

#         user = profile.__class__.objects.get(phone=phone)
#         current_time = timezone.now()
#         if user.Otpcreated_at and user.Otpcreated_at > current_time:
#             user.otp = random.randint(1000, 9999)
#             user.Otpcreated_at = current_time + timedelta(minutes=5)
#         else:
#             user.otp = random.randint(1000, 9999)
#             user.Otpcreated_at = current_time + timedelta(minutes=5)

#         user.save()
#         # send_otp_on_phone(user.phone, user.otp)
#         return Response({'uid': str(user.uid), 'otp': str(user.otp), 'message': "Otp sent successfully"})


# class Otp(APIView):
#     serializer_class = OtpSerializer

#     def post(self, request, uid):
#         serializer = self.serializer_class(data=request.data)
#         otp = serializer.initial_data.get('otp')
#         profiles = [Audio_Jockey, Coins_club_owner,
#                     Coins_trader, Jockey_club_owner, User]
#         profile = None

#         for profile_model in profiles:
#             try:
#                 profile = profile_model.objects.get(uid=uid)
#                 break
#             except profile_model.DoesNotExist:
#                 continue

#         current_time = timezone.now()
#         if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
#             user_serializer = UserSerializer(profile)
#             return Response({'data': {'data': (user_serializer.data), 'profile': (profile.__class__.__name__), 'id': (profile.id),  'access': str(profile.token), 'message': "Login successfully"}})
#         else:
#             return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)


# from twilio.rest import Client
# from django.conf import settings
# from decouple import config
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from datetime import timedelta
# import random
# from django.utils import timezone

# # Load Twilio credentials from environment variables
# account_sid = config('account_sid')
# auth_token = config('auth_token')
# twilio_phone_number = config('twilio_phone_number')

# # Helper function to send OTP via Twilio
# def send_otp_on_phone(phone_number, otp):
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#         body=f"Your OTP is {otp}",
#         from_=twilio_phone_number,
#         to=phone_number
#     )
#     return message.sid  # Return the message SID for logging or further tracking if needed

# class Login(APIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         phone = serializer.initial_data.get('phone')

#         profiles = [Audio_Jockey, Coins_club_owner,
#                     Coins_trader, Jockey_club_owner, User]
#         profile = None

#         for profile_model in profiles:
#             profile = profile_model.objects.filter(phone=phone).first()
#             if profile:
#                 break

#         if not profile:
#             return Response({'message': "No user found with this mobile"}, status=status.HTTP_404_NOT_FOUND)

#         if hasattr(profile, 'Is_Approved') and not profile.Is_Approved:
#             return Response({'message': f"{profile.__class__.__name__} {profile} is not approved Yet. Please wait for some time to get approved."}, status=status.HTTP_403_FORBIDDEN)

#         user = profile.__class__.objects.get(phone=phone)
#         current_time = timezone.now()
#         otp = random.randint(1000, 9999)

#         if user.Otpcreated_at and user.Otpcreated_at > current_time:
#             user.otp = otp
#             user.Otpcreated_at = current_time + timedelta(minutes=5)
#         else:
#             user.otp = otp
#             user.Otpcreated_at = current_time + timedelta(minutes=5)

#         user.save()

#         # Send OTP via SMS
#         send_otp_on_phone(user.phone, user.otp)

#         return Response({'uid': str(user.uid), 'otp': str(user.otp), 'message': "Otp sent successfully"})

# class Otp(APIView):
#     serializer_class = OtpSerializer

#     def post(self, request, uid):
#         serializer = self.serializer_class(data=request.data)
#         otp = serializer.initial_data.get('otp')
#         profiles = [Audio_Jockey, Coins_club_owner,
#                     Coins_trader, Jockey_club_owner, User]
#         profile = None

#         for profile_model in profiles:
#             try:
#                 profile = profile_model.objects.get(uid=uid)
#                 break
#             except profile_model.DoesNotExist:
#                 continue

#         current_time = timezone.now()
#         if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
#             user_serializer = UserSerializer(profile)
#             return Response({'data': {'data': (user_serializer.data), 'profile': (profile.__class__.__name__), 'id': (profile.id),  'access': str(profile.token), 'message': "Login successfully"}})
#         else:
#             return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)

from twilio.rest import Client
from django.conf import settings
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
import random
from django.utils import timezone

# Load Twilio credentials from environment variables
account_sid = config('account_sid')
auth_token = config('auth_token')
twilio_phone_number = config('twilio_phone_number')

# Special number and OTP
SPECIAL_OTP = '6666'

# Helper function to send OTP via Twilio
# List of special numbers
SPECIAL_NUMBERS = ['+915689745325', '+917564839102', '+919876543210', '+916261709525', '+910000000000']  # Add more special numbers as needed

def send_otp_on_phone(phone_number, otp):
    # Send OTP only if the number is NOT in the special numbers list
    if phone_number not in SPECIAL_NUMBERS:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP is {otp}",
            from_=twilio_phone_number,
            to=phone_number
        )
        return message.sid  # Return the message SID for logging or further tracking if needed
    return None  # Skip sending SMS for special numbers

class Login(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        phone = serializer.initial_data.get('phone')

        # Check if user already exists
        profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
        profile = None

        for profile_model in profiles:
            profile = profile_model.objects.filter(phone=phone).first()
            if profile:
                break

        current_time = timezone.now()

        if not profile:
            # AUTO-CREATE a new User with this phone number
            uid = uuid.uuid1()
            token = secrets.token_hex(128)
            otp = SPECIAL_OTP if phone in SPECIAL_NUMBERS else random.randint(1000, 9999)
            # email=f"antima@gmail.com"
            email = f"user_{phone}@example.com"

            user = User.objects.create(
                phone=phone,
                uid=uid,
                token=token,
                otp=otp,
                email=email,
                Otpcreated_at=current_time + timedelta(minutes=5),
                Is_Approved=True,
                usertype="User"
            )

            Common.objects.create(
                uid=uid,
                token=token,
                usertype="User",
                Is_Approved=True
            )

            send_otp_on_phone(user.phone, otp)

            return Response({
                'uid': str(uid),
                'otp': str(otp),
                'message': "OTP sent successfully and user created"
            })

        # User exists → update OTP
        user = profile.__class__.objects.get(phone=phone)
        otp = SPECIAL_OTP if phone in SPECIAL_NUMBERS else random.randint(1000, 9999)
        user.otp = otp
        user.Otpcreated_at = current_time + timedelta(minutes=5)
        user.save()

        send_otp_on_phone(user.phone, otp)

        return Response({
            'uid': str(user.uid),
            'otp': str(user.otp),
            'message': "OTP sent successfully"
        })

# class Otp(APIView):
#     serializer_class = OtpSerializer

#     def post(self, request, uid):
#         serializer = self.serializer_class(data=request.data)
#         otp = serializer.initial_data.get('otp')
#         profiles = [Audio_Jockey, Coins_club_owner,
#                     Coins_trader, Jockey_club_owner, User]
#         profile = None

#         for profile_model in profiles:
#             try:
#                 profile = profile_model.objects.get(uid=uid)
#                 break
#             except profile_model.DoesNotExist:
#                 continue

#         current_time = timezone.now()
#         if otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
#             user_serializer = UserSerializer(profile)
#             return Response({'data': {'data': (user_serializer.data), 'profile': (profile.__class__.__name__), 'id': (profile.id),  'access': str(profile.token), 'message': "Login successfully"}})
#         else:
#             return Response({'message': "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)

class Otp(APIView):
    serializer_class = OtpSerializer

    def post(self, request, uid):
        serializer = self.serializer_class(data=request.data)
        otp = serializer.initial_data.get('otp')
        profiles = [Audio_Jockey, Coins_club_owner,
                    Coins_trader, Jockey_club_owner, User]
        profile = None

        for profile_model in profiles:
            try:
                profile = profile_model.objects.get(uid=uid)
                break
            except profile_model.DoesNotExist:
                continue

        current_time = timezone.now()

        # If profile exists, verify OTP
        if profile and otp == profile.otp and profile.Otpcreated_at and profile.Otpcreated_at > current_time:
            user_serializer = UserSerializer(profile)
            return Response({
                'data': {
                    'data': user_serializer.data,
                    'profile': profile.__class__.__name__,
                    'id': profile.id,
                    'access': str(profile.token),
                    'message': "Login successfully"
                }
            })

        # ✅ If user does not exist, auto-create one
        if not profile and otp == SPECIAL_OTP:  # only allow special OTP to create new for now
            token = secrets.token_hex(128)
            uid = uuid.uuid1()
            phone = request.data.get('phone')  # phone must be sent again
            if not phone:
                return Response({'message': "Phone number is required for auto-registration."}, status=400)

            user = User.objects.create(
                phone=phone,
                otp=otp,
                token=token,
                uid=uid,
                Is_Approved=True,
                usertype="User",
                Otpcreated_at=current_time + timedelta(minutes=5)
            )
            Common.objects.create(
                uid=uid,
                token=token,
                usertype="User",
                Is_Approved=True
            )

            user_serializer = UserSerializer(user)
            return Response({
                'data': {
                    'data': user_serializer.data,
                    'profile': "User",
                    'id': user.id,
                    'access': str(token),
                    'message': "User auto-created and logged in successfully"
                }
            })

        return Response({'message': "Invalid OTP or expired. Please try again."}, status=status.HTTP_400_BAD_REQUEST)



class UpdateUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, format=None):
        pk = request.user.uid
        user = User.objects.get(uid=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    @method_decorator(authenticate_token)
    def put(self, request, format=None):
        uid = request.user.uid
        user = get_object_or_404(User, uid=uid)
        common_objects = Common.objects.get(uid=uid)
        print(common_objects)
        serializer = UserUpdateSerializer(user, data=request.data)
        if common_objects:
            serializer1 = masterUpdateSerializer(common_objects, data=request.data)
            if serializer1.is_valid():
                serializer1.save()

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @method_decorator(authenticate_token)
    def delete(self, request, format=None):
        pk = request.user.uid
        user = User.objects.get(uid=pk)
        commonuser = Common.objects.get(uid=pk)
        if commonuser:
            commonuser.delete()
            user.delete()
            return Response({"delete":"successfully"})
        return Response({"delete":"unsuccessfully"})
    
class GetUserdata(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = GetUserSerializer(user)
            user_data = serializer.data
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow.objects.filter(user=user).count()


class Searchalluser(ListAPIView):
    serializer_class = UserSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['Name', 'email']

    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = User.objects.exclude(id=self.request.user.id)
        user = self.request.user
        if user:
            queryset = self.annotate_following(queryset, user)
        return queryset

    def annotate_following(self, queryset, user):
        for user_obj in queryset:
            user_obj.is_following = Follow.objects.filter(
                user=user, following_user=user_obj).exists()
        return queryset


class GetUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, Userid):
        try:
            user = User.objects.get(id=Userid)
            serializer = GetUserSerializer(user)
            user_data = serializer.data

            posts = Post5.objects.filter(user=user)
            images = [post.image.url for post in posts if post.image]  # Collect image URLs from posts

            # Add images field (list of image URLs from posts)
            user_data['images'] = images
            user_data['is_followed'] = self.is_followed(user, request.user)
            user_data['follower_count'] = self.get_follower_count(user)
            user_data['following_count'] = self.get_following_count(user)
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    def is_followed(self, user, current_user):
        return Follow.objects.filter(user=current_user, following_user=user).exists()

    def get_follower_count(self, user):
        return Follow.objects.filter(following_user=user).count()

    def get_following_count(self, user):
        return Follow.objects.filter(user=user).count()


class FollowUser(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, follow):
        try:
            following_user = User.objects.get(id=follow)
            follow_user, created = Follow.objects.get_or_create(
                user=request.user, following_user=following_user)

            if not created:
                follow_user.delete()
                return Response({'success': True, 'message': 'Unfollowed user'})
            else:
                return Response({'success': True, 'message': 'Followed user'})

        except User.DoesNotExist:
            return Response({'success': False, 'message': 'User does not exist.'})


class FollowerList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user  
        followers = Follow.objects.filter(following_user=user)
        followed_users = Follow.objects.filter(user=user, following_user__in=followers.values_list('user', flat=True))
        
        queryset = self.annotate_followers(followers, followed_users)
        serializer = getfollowerSerializer(queryset, many=True)
        
        return Response(serializer.data)

    def annotate_followers(self, followers, followed_users):
        user_dict = {}
        followed_users_set = set(followed_users.values_list('following_user', flat=True))
        
        for follower in followers:
            following_user = follower.user
            user_dict[following_user.id] = {
                "id": following_user.id,
                "Name": following_user.Name,
                "email": following_user.email,
                "Gender": following_user.Gender,
                "Dob": following_user.Dob,
                "profile_picture": following_user.profile_picture,
                "Introduction_voice": following_user.Introduction_voice,
                "Introduction_text": following_user.Introduction_text,
                "is_followed": following_user.id in followed_users_set
            }
        
        return list(user_dict.values())


class FollowingList(APIView):
    @method_decorator(authenticate_token)
    def get(self, request, *args, **kwargs):
        following = Follow.objects.filter(user=request.user)
        followed_users = [follow_obj.following_user for follow_obj in following]

        user_data_list = []
        for user in followed_users:
            user_data = {
                "id": user.id,
                "Name": user.Name,
                "email": user.email,
                "Gender": user.Gender,
                "Dob": user.Dob,
                "profile_picture": user.profile_picture,
                "Introduction_voice": user.Introduction_voice,
                "Introduction_text": user.Introduction_text,
                "is_followed": True  
            }
            user_data_list.append(user_data)

        return Response(user_data_list)


@method_decorator(authenticate_token, name='dispatch')
class userview(APIView):
    def get(self, request):
        user = request.user
        print(user)
        return JsonResponse({'uid': user.uid, 'number': user.phone, "name": user.Name})
    
class Alluser(APIView):
    def get(self,request):
        data=User.objects.all()
        serialiser = UserSerializer(data,many=True)
        return Response(serialiser.data)




class Socialmedia(APIView):
    serializer_class = SocialmediaSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            my_dict=serializer.data
            return Response({"Social_media_id":my_dict}, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Googlelogin(APIView):
    serializer_class = GoogleLoginSerializer
    def post(self,request):
        profile = None
        serializer = self.serializer_class(data=request.data)
        google = serializer.initial_data.get('Google')
        profile = Social_media.objects.filter(Google=google).first()

        if not profile:
            return Response({'message': 'No user found with this Google ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
        for profile_model in profiles:
                try:
                    profile_data = profile_model.objects.filter(email=profile.Google).first()
                    if profile_data:
                        break
                except profile_model.DoesNotExist:
                    continue
        if profile.Google==google:
            user =UserSerializer(profile_data)
            return Response({'data': {'data': (user.data), 'profile': (profile_data.__class__.__name__), 'id': (profile_data.id),  'access': str(profile_data.token), 'message': "Login successfully with Google"}})



class Facebooklogin(APIView):
    serializer_class = FacebookLoginSerializer
    def post(self,request):
        profile = None
        serializer = self.serializer_class(data=request.data)
        Facebook_id = serializer.initial_data.get('Facebook')
        
        profile = Social_media.objects.filter(Facebook=Facebook_id).first()
        
        if not profile:
            return Response({'message': 'No user found with this Facebook ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
        for profile_model in profiles:
                try:
                    profile_data = profile_model.objects.filter(email=profile.Facebook).first()

                    if profile_data:
                        break
                except profile_model.DoesNotExist:
                    continue
        if profile.Facebook==Facebook_id:
            user =UserSerializer(profile_data)
            return Response({'data': {'data': (user.data), 'profile': (profile_data.__class__.__name__), 'id': (profile_data.id),  'access': str(profile_data.token), 'message': "Login successfully with Facebook"}})
        else:
            return Response({"message":"invalid"})
        


class Snapchatlogin(APIView):
    serializer_class = SnapchatLoginSerializer
    def post(self,request):
        profile = None
        serializer = self.serializer_class(data=request.data)
        Snapchat_id = serializer.initial_data.get('Snapchat')
        
        profile = Social_media.objects.filter(Snapchat=Snapchat_id).first()
        
        if not profile:
            return Response({'message': 'No user found with this Facebook ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        profiles = [Audio_Jockey, Coins_club_owner,Coins_trader, Jockey_club_owner, User]
        for profile_model in profiles:
                try:
                    profile_data = profile_model.objects.filter(email=profile.Snapchat).first()

                    if profile_data:
                        break
                except profile_model.DoesNotExist:
                    continue
        if profile.Snapchat==Snapchat_id:
            user =UserSerializer(profile_data)
            return Response({'data': {'data': (user.data), 'profile': (profile_data.__class__.__name__), 'id': (profile_data.id),  'access': str(profile_data.token), 'message': "Login successfully with Snapchat"}})
        else:
            return Response({"message":"invalid"})





class Coinsclaim(APIView):
    serialiser_class = CoinsclaimSerializer
    @method_decorator(authenticate_token)
    def post(self,request):
        serialiser = self.serialiser_class(data = request.data)
        if serialiser .is_valid():
            claim = serialiser.initial_data.get('claim_coins')
            created_at = datetime.today()#datetime.today()
            print('created_at',created_at)
            if claim:
                today_claimed_count = claim_coins.objects.filter(
                    user=request.user,
                    created_date__date=created_at.date()).count()
                print(today_claimed_count)
                if today_claimed_count==0:
                    user = User.objects.get(token=request.user.token)
                    user.coins += 10
                    user.save()
                    common_profile = Common.objects.get(token=request.user.token)
                    message = f"You got {10} coins to logging in today!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    claim_coins.objects.create(user=request.user,created_date=created_at, claim_coins=True)
                    return Response({"data": f"{10}Coins added successfully"})
                return Response({"data":"You have already claimed coins today."})
            return Response({"data":"data"})



class Coins_club_ownerdaliyclaim(APIView):
    serialiser_class = Coins_club_ownerdaliyclaimSerializer
    @method_decorator(authenticate_token)
    def post(self,request):
        serialiser = self.serialiser_class(data = request.data)
        if serialiser .is_valid():
            claim = serialiser.initial_data.get('claim_coins')
            created_at = datetime.today()
            print('created_at',created_at)
            if claim:
                today_claimed_count = Coinsclubownerdaliylogin.objects.filter(user=request.user,created_date__date=created_at.date()).count()
                print(today_claimed_count)
                if today_claimed_count==0:
                    user = Coins_club_owner.objects.get(token=request.user.token)
                    user.coins += 10
                    user.save()
                    common_profile = Common.objects.get(token=request.user.token)
                    message = f"You got {10} coins to logging in today!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    Coinsclubownerdaliylogin.objects.create(user=request.user,created_date=created_at, claim_coins=True)
                    return Response({"data": f"{10}Coins added successfully"})
                return Response({"data":"You have already claimed coins today."})
            return Response({"data":"data"})



class Coinstraderdaliyclaim(APIView):
    serialiser_class = Coins_traderdaliyclaimSerializer
    @method_decorator(authenticate_token)
    def post(self,request):
        serialiser = self.serialiser_class(data = request.data)
        if serialiser .is_valid():
            claim = serialiser.initial_data.get('claim_coins')
            created_at = datetime.today()
            print('created_at',created_at)
            if claim:
                today_claimed_count = Coins_traderdaliylogin.objects.filter(
                    user=request.user,
                    created_date__date=created_at.date()).count()
                print(today_claimed_count)
                if today_claimed_count==0:
                    user = Coins_trader.objects.get(token=request.user.token)
                    user.coins += 10
                    user.save()
                    common_profile = Common.objects.get(token=request.user.token)
                    message = f"You got {10} coins to logging in today!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    Coins_traderdaliylogin.objects.create(user=request.user,created_date=created_at, claim_coins=True)
                    return Response({"data": f"{10}Coins added successfully"})
                return Response({"data":"You have already claimed coins today."})
            return Response({"data":"data"})


class Jockey_club_ownerdaliyclaim(APIView):
    serialiser_class = Jockey_club_ownerdaliyclaimSerializer
    @method_decorator(authenticate_token)
    def post(self,request):
        serialiser = self.serialiser_class(data = request.data)
        if serialiser .is_valid():
            claim = serialiser.initial_data.get('claim_coins')
            created_at = datetime.today()
            print('created_at',created_at)
            if claim:
                today_claimed_count = Jockeyclubownerlogin.objects.filter(
                    user=request.user,
                    created_date__date=created_at.date()).count()
                print(today_claimed_count)
                if today_claimed_count==0:
                    user = Jockey_club_owner.objects.get(token=request.user.token)
                    user.coins += 10
                    user.save()
                    common_profile = Common.objects.get(token=request.user.token)
                    message = f"You got {10} coins to logging in today!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    Jockeyclubownerlogin.objects.create(user=request.user,created_date=created_at, claim_coins=True)
                    return Response({"data": f"{10}Coins added successfully"})
                return Response({"data":"You have already claimed coins today."})
            return Response({"data":"data"})


class Audio_Jockeydaliyclaim(APIView):
    serialiser_class = Audio_JockeydaliyclaimSerializer
    @method_decorator(authenticate_token)
    def post(self,request):
        print("pass king")
        serialiser = self.serialiser_class(data = request.data)
        if serialiser .is_valid():
            claim = serialiser.initial_data.get('claim_coins')
            created_at = datetime.today()
            print('created_at',created_at)
            if claim:
                today_claimed_count = Audiojockeyloigin.objects.filter(
                    user=request.user,
                    created_date__date=created_at.date()).count()
                print(today_claimed_count)
                if today_claimed_count==0:
                    user = Audio_Jockey.objects.get(token=request.user.token)
                    user.coins += 10
                    user.save()
                    common_profile = Common.objects.get(token=request.user.token)
                    message = f"You got {10} coins to logging in today!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    Audiojockeyloigin.objects.create(user=request.user,created_date=created_at, claim_coins=True)
                    return Response({"data": f"{10}Coins added successfully"})
                return Response({"data":"You have already claimed coins today."})
            return Response({"data":"data"})


class RazorpayOrderAPIView(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        razorpay_order_serializer = RazorpayOrderSerializer(data=request.data)
        if razorpay_order_serializer.is_valid():
            order_response = rz_client.create_order(
                amount=razorpay_order_serializer.validated_data.get("amount"),
                currency=razorpay_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



# class TransactionAPIView(APIView):
#     @method_decorator(authenticate_token)
#     def post(self, request):
#         transaction_serializer = Transactionmodelserializer(data=request.data)
#         if transaction_serializer.is_valid():
#             rz_client.verify_payment_signature(
#                 razorpay_payment_id = transaction_serializer.validated_data.get("payment_id"),
#                 razorpay_order_id = transaction_serializer.validated_data.get("order_id"),
#                 razorpay_signature = transaction_serializer.validated_data.get("signature")
#             )
            
#             amount = transaction_serializer.validated_data.get("amount")
#             ruppees=amount//100
#             coin_s= ruppees*10
#             print("ruppees",ruppees)
#             print("coin_s",coin_s)
#             created_date = datetime.today()
#             if amount == 10000:
#                 profiles = [Audio_Jockey, Coins_club_owner, Coins_trader, Jockey_club_owner, User]
#                 for profile_model in profiles:
#                     user_profile = profile_model.objects.filter(token=request.user.token).first()
#                     if isinstance(user_profile, User):
#                         user_profile = User.objects.get(token=request.user.token)
#                         user_profile.coins += 1000
#                         user_profile.save()
#                         common_profile = Common.objects.get(token=request.user.token)
#                         message = f"You got {1000} coins on recharge of Rs 100!"
#                         notification = Notificationupdate(user=common_profile, message=message)
#                         notification.save()
#                         Purchase_history.objects.create(user=common_profile,created_date=created_date, claim_coins=True)
#                     elif isinstance(user_profile, Audio_Jockey):
#                         user_profile = Audio_Jockey.objects.get(token=request.user.token)
#                         user_profile.coins += 1000 
#                         user_profile.save()
#                         common_profile = Common.objects.get(token=request.user.token)
#                         message = f"You got {1000} coins on recharge of Rs 100!"
#                         notification = Notificationupdate(user=common_profile, message=message)
#                         notification.save()
#                         Purchase_history.objects.create(user=common_profile,created_date=created_date, claim_coins=True)
#                     elif isinstance(user_profile, Jockey_club_owner):
#                         user_profile = Jockey_club_owner.objects.get(token=request.user.token)
#                         user_profile.coins += 1000 
#                         user_profile.save()
#                         common_profile = Common.objects.get(token=request.user.token)
#                         message = f"You got {1000} coins on recharge of Rs 100!"
#                         notification = Notificationupdate(user=common_profile, message=message)
#                         notification.save()
#                         Purchase_history.objects.create(user=common_profile,created_date=created_date, claim_coins=True)
#                     elif isinstance(user_profile, Coins_trader):
#                         user_profile = Coins_trader.objects.get(token=request.user.token)
#                         user_profile.coins += 1000 
#                         user_profile.save()
#                         common_profile = Common.objects.get(token=request.user.token)
#                         message = f"You got {1000} coins on recharge of Rs 100!"
#                         notification = Notificationupdate(user=common_profile, message=message)
#                         notification.save()
#                         Purchase_history.objects.create(user=common_profile,created_date=created_date, claim_coins=True)
#                     elif isinstance(user_profile, Coins_club_owner):
#                         user_profile = Coins_club_owner.objects.get(token=request.user.token)
#                         user_profile.coins += 1000 
#                         user_profile.save()
#                         common_profile = Common.objects.get(token=request.user.token)
#                         message = f"You got {1000} coins on recharge of Rs 100!"
#                         notification = Notificationupdate(user=common_profile, message=message)
#                         notification.save()
#                         Purchase_history.objects.create(user=common_profile,created_date=created_date, claim_coins=True)
#             else:
#                 return Response({"message": "Transaction processed, but no bonus coins added."}, status=status.HTTP_200_OK)        
#             transaction_serializer.save()
            
#             return Response({"message": "transaction created"}, status=status.HTTP_201_CREATED)
#         else:
#             response = {
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "message": "bad request",
#                 "error": transaction_serializer.errors
#             }
#             return Response(response, status=status.HTTP_400_BAD_REQUEST)

  
class TransactionAPIView(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        transaction_serializer = Transactionmodelserializer(data=request.data)
        if transaction_serializer.is_valid():
            try:
                rz_client.verify_payment_signature(
                    razorpay_payment_id=transaction_serializer.validated_data.get("payment_id"),
                    razorpay_order_id=transaction_serializer.validated_data.get("order_id"),
                    razorpay_signature=transaction_serializer.validated_data.get("signature")
                )
            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            
            amount = transaction_serializer.validated_data.get("amount")
            rupees = amount // 100
            coins = rupees * 10

            created_date = datetime.today()
            common_profile = Common.objects.get(token=request.user.token)
            user_profiles = [User,Audio_Jockey,Jockey_club_owner,Coins_trader,Coins_club_owner]
            for model_class in user_profiles:
                user_profile = model_class.objects.filter(token=request.user.token).first()
                if isinstance(user_profile, model_class):
                    print("user_profile",user_profile)
                    user_profile.coins += coins
                    user_profile.save()
                    message = f"You got {coins} coins on recharge of Rs {rupees}!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()
                    Purchase_history.objects.create(user=common_profile, created_date=created_date, claim_coins=message)
            transaction_serializer.save()

            return Response({"message": "Transaction created"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Bad request", "error": transaction_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


###############3
############
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post5
from .serializers import PostSerializer
from datetime import datetime
from django.utils.decorators import method_decorator


class TotalPostCount(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user
        post_count = Post5.objects.filter(user=user).count()
        return Response({'post_count': post_count})

class UploadPost(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        try:
            text = request.data.get('text', None)
            image = request.FILES.get('image', None)
            video = request.FILES.get('video', None)
            user = request.user  # Get the authenticated user

            if not text and not image and not video:
                return Response({"error": "Post must have text or media (image/video)."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the post
            post = Post5(user=user, text=text)

            if image:
                post.image = image
            if video:
                post.video = video
            
            post.save()

            # Add 20 coins to the user profile
            user_profile = User.objects.filter(token=user.token).first()
            if user_profile:
                user_profile.coins += 20  # Add 20 coins
                user_profile.save()

                # Get the corresponding Common instance
                common_profile = Common.objects.filter(token=user.token).first()
                
                if common_profile:
                    # Optionally, you can create a notification for the user about the added coins
                    message = "You have received 20 coins for uploading a post!"
                    notification = Notificationupdate(user=common_profile, message=message)
                    notification.save()

            return Response({'success': 'Post uploaded successfully and 20 coins added.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post5, Follow  # Assuming Follow is your follow model
from .serializers import PostSerializer
from datetime import datetime
from django.utils.decorators import method_decorator
# from .authentication import authenticate_token  # Ensure this import is correct

class GetPosts(APIView):
    @method_decorator(authenticate_token)
    def get(self, request):
        user = request.user
        
        # Get the list of users that the current user is following
        following = Follow.objects.filter(user=user).values_list('following_user', flat=True)
        
        # We will only show posts from the user whose token was provided, so no need to add following users here
        # Fetch only posts from the logged-in user, excluding those of the users they follow
        posts = Post5.objects.filter(user=user).order_by('-created_at')
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data)

    @method_decorator(authenticate_token)
    def delete(self, request, post_id):
        user = request.user
        
        try:
            # Try to retrieve the post by ID
            post = Post5.objects.get(id=post_id)
        except Post5.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the logged-in user is the owner of the post
        if post.user != user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete the post
        post.delete()
        
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


#last api in django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from User.models import User
from coin.models import Gift  # ✅ सही Gift model जिसमें `gift_image` और `price` है

@method_decorator(csrf_exempt, name='dispatch')
class SendGiftAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print("REQUEST DATA:", request.data)
        print("CONTENT TYPE:", request.content_type)

        sender_id   = request.data.get('sender_id')
        receiver_id = request.data.get('receiver_id')
        gift_id     = request.data.get('gift_id')
        
        if not all([sender_id, receiver_id, gift_id]):
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        sender   = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)
        gift     = get_object_or_404(Gift, id=gift_id)

        # ✅ Correct field: gift.price (na ki gift.coins)
        if sender.coins < gift.price:
            return Response({'error': 'Not enough coins'}, status=status.HTTP_400_BAD_REQUEST)

        sender.coins   -= gift.price
        receiver.coins += gift.price
        sender.save()
        receiver.save()

        return Response({
            'message': 'Gift sent successfully',
            'gift': {
                'id': gift.id,
                'image_url': request.build_absolute_uri(gift.gift_image.url),  # ✅ image field ka URL
                'price': gift.price
            },
            'sender_coins': sender.coins,
            'receiver_coins': receiver.coins
        }, status=status.HTTP_200_OK)
    
class Userlevel(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        coins = user.coins
        level = Wealthlevel.get_user_level(coins)

        if not level:
            return Response({"error": "Wealth level not found for this coin range"}, status=404)

        return Response({
            "user_id": user.id,
            "user_name": user.Name,
            "coins": coins,
            "level": level.level,
            "badge": level.badge
        }, status=200)


#wealth level according to razorpay


from rest_framework import viewsets
class Frameset(viewsets.ModelViewSet):
    queryset=Frames.objects.all()
    serializer_class = FramesSerializer
    
from .models import Frames, PurchasedFrame

# class PurchaseFrameAPIView(APIView):
#     @authenticate_token
#     def post(self, request):
#         user = request.user
#         frame_id = request.data.get('frame_id')

#         frame = get_object_or_404(Frames, id=frame_id)

#         # ✅ Check if user already purchased this frame
#         if PurchasedFrame.objects.filter(user=user, frame=frame).exists():
#             return Response({'error': 'You have already purchased this frame.'}, status=status.HTTP_400_BAD_REQUEST)

#         if user.coins < frame.price_in_coins:
#             return Response({'error': 'Not enough coins.'}, status=status.HTTP_400_BAD_REQUEST)

#         with transaction.atomic():
#             user.coins -= frame.price_in_coins
#             user.save()

#             # ✅ Record the purchase
#             PurchasedFrame.objects.create(user=user, frame=frame)

#         return Response({'message': 'Frame purchased successfully!'}, status=status.HTTP_200_OK)



from django.db import transaction

class PurchaseFrameAPIView(APIView):
    # @authenticate_token
    @method_decorator(authenticate_token)
    def post(self, request):
        user = request.user
        frame_id = request.data.get('frame_id')
        frame = get_object_or_404(Frames, id=frame_id)

        if PurchasedFrame.objects.filter(user=user, frame=frame).exists():
            return Response({'error': 'You already purchased this frame.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.coins < frame.coins:
            return Response({'error': 'Not enough coins.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user.coins -= frame.coins
                user.save()
                PurchasedFrame.objects.create(user=user, frame=frame)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
    'message': 'Frame purchased successfully',
    'frame_name': frame.name,
    'frame_cost': frame.coins,
    'user_name':user.Name,
    'user_remaining_coins': user.coins
}, status=status.HTTP_200_OK)
    

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class CreateFamilyAPIView(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        user = request.user

        # Check if user is already in a family
        if FamilyMember.objects.filter(user=user).exists():
            return Response({'error': 'You are already part of a family.'}, status=status.HTTP_400_BAD_REQUEST)

        family_name = request.data.get('family_name')
        family_tag = request.data.get('family_tag')
        family_announcement = request.data.get('family_announcement')

        # Create family and set user as admin
        family = Family.objects.create(
            family_name=family_name,
            family_tag=family_tag,
            family_announcement=family_announcement,
            admin=user
        )

        # Add admin as a member
        FamilyMember.objects.create(user=user, family=family)

        return Response({'message': 'Family created successfully.'}, status=status.HTTP_201_CREATED)

class JoinFamilyAPIView(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        user = request.user
        family_id = request.data.get('family_id')

        if FamilyMember.objects.filter(user=user).exists():
            return Response({'error': 'You already belong to a family.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            family = Family.objects.get(id=family_id)
        except Family.DoesNotExist:
            return Response({'error': 'Family not found.'}, status=status.HTTP_404_NOT_FOUND)

        FamilyMember.objects.create(user=user, family=family)
        return Response({'message': 'Joined family successfully.'}, status=status.HTTP_200_OK)
    
class LeaveFamilyAPIView(APIView):
    @method_decorator(authenticate_token)
    def post(self, request):
        user = request.user

        try:
            membership = FamilyMember.objects.get(user=user)
        except FamilyMember.DoesNotExist:
            return Response({'error': 'You are not part of any family.'}, status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        return Response({'message': 'You have left the family successfully.'}, status=status.HTTP_200_OK)
class DeleteFamilyAPIView(APIView):
    @method_decorator(authenticate_token)
    def delete(self, request):
        user = request.user

        try:
            family = Family.objects.get(admin=user)
        except Family.DoesNotExist:
            return Response({'error': 'You are not an admin of any family.'}, status=status.HTTP_403_FORBIDDEN)

        members = FamilyMember.objects.filter(family=family)
        for member in members:
            member_user = member.user         
        
        
        members.delete()
        family.delete()

        return Response({'message': 'Family and all memberships deleted successfully.'}, status=status.HTTP_200_OK)
