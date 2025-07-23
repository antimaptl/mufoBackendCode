from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Profile
from .serializers import OTPVerifySerializer
from django.conf import settings
from twilio.rest import Client
import random

HARD_CODED_NUMBER = "+915689745325"
HARD_CODED_OTP = "6666"

class OTPRequestView(APIView):
    def post(self, request):
        mobile_number = request.data.get('mobile_number')
        if not mobile_number:
            return Response({"message": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Use hardcoded OTP for test number
        if mobile_number == HARD_CODED_NUMBER:
            otp = HARD_CODED_OTP
        else:
            otp = str(random.randint(1000, 9999))  # Generate random OTP

        # Save or create user/profile with OTP
        user, _ = User.objects.get_or_create(username=mobile_number)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.otp = otp
        profile.save()

        # Send OTP via Twilio only for non-test numbers
        if mobile_number != HARD_CODED_NUMBER:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=f"Your OTP is {otp}",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=mobile_number
                )
            except Exception as e:
                return Response({"message": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": f"OTP sent to {mobile_number}"}, status=status.HTTP_200_OK)

class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = serializer.validated_data['otp']

            try:
                user = User.objects.get(username=mobile_number)
                profile = Profile.objects.get(user=user)

                # Validate OTP (hardcoded or random)
                if mobile_number == HARD_CODED_NUMBER and otp == HARD_CODED_OTP:
                    pass
                elif otp != profile.otp:
                    return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                profile.otp = None  # Invalidate OTP
                profile.save()

                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)

            except (User.DoesNotExist, Profile.DoesNotExist):
                return Response({"message": "User or OTP not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# authentication/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Person
from .serializers import PersonSerializer

class PersonCRUDView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        persons = Person.objects.filter(user=request.user)
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            person = Person.objects.get(pk=pk, user=request.user)
        except Person.DoesNotExist:
            return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            person = Person.objects.get(pk=pk, user=request.user)
        except Person.DoesNotExist:
            return Response({"message": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
