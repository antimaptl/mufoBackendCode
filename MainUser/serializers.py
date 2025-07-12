# authentication/serializers.py
from rest_framework import serializers

class OTPVerifySerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=10)


# authentication/serializers.py
from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'email', 'password', 'gender', 'dob', 'mobile_no', 'profile_picture']

