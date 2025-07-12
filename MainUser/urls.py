# authentication/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('request-otp/', OTPRequestView.as_view(), name='request_otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('persons/', PersonCRUDView.as_view()),              # GET all, POST new
    path('persons/<int:pk>/', PersonCRUDView.as_view()), 
]
