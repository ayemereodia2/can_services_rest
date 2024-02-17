from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from google.auth.transport import requests
from google.oauth2 import id_token
from django.db import models

from allauth.account.models import EmailAddress
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
import random
from can_backend.utils import Utils
from .serializers import CustomUser, EmailSerializer


# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# import requests
from .serializers import UserSerializer

class UserCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer(data=request.data)

        data = {}
        
        if serializer_class.is_valid():
            email = serializer_class.validated_data['email']
            password = serializer_class.validated_data['password']
            
            if GoogleTokenValidator.check_user_email_exists(email):
                data['response'] = 'user account already exist'
                return Response(data, status=status.HTTP_201_CREATED)
            
                
            user = CustomUser.objects.create_user_with_otp(email= email, password=password)
            data['response'] = 'user account created'
            data['username'] = user.email
            return Response(data, status=status.HTTP_201_CREATED)
        data = serializer_class.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
class ResendOTP(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = GoogleTokenValidator.get_user_with(email)

            if user:
                otp = self.generate_otp()
                self.update_user_otp(user, otp)
                self.send_otp_email(email, otp)
                return Response({'response': 'OTP sent'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'response': 'User account does not exist'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_otp(self):
        return ''.join(random.choices('0123456789', k=6))

    def update_user_otp(self, user, otp):
        user.otp = otp
        user.save()

    def send_otp_email(self, email, otp):
        email_body = f'Hi there, you are trying to use the Qway App!\nPlease use the following One Time Password (OTP) to verify your email address:\n\n{otp}'
        data = {'subject': 'Verify your email address', 'email_body': email_body, 'recipient': email}
        Utils.send_email(data)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = GoogleTokenValidator.get_user_with(email=email)
        
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'message': f'{user.email} is not a verified email address' })

class VerifyOTPView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = GoogleTokenValidator.get_user_with(email=email)

        if user:
            if user.otp == otp and user.is_active == False:
                return self.update_user_property(user=user,new_value= True)
            else:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Empty Body or User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def update_user_property(self, user, new_value):
        try:
            # Retrieve the user object from the database
            if user:
                # Update the specified property
                setattr(user, 'is_active', new_value)
                # Save the user object to persist the changes
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }, status=status.HTTP_200_OK)
                
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
   
class GoogleTokenValidator(APIView):

    def post(self, request):
        try:
            token = request.data.get("idToken")
            client_id = '806876359059-esi3hlama0nsomlvo479qchpqlqgdnln.apps.googleusercontent.com'

            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

            userid = idinfo['sub']
            email = idinfo['email']
            name = idinfo['name']
            print("user", userid, email, name)
            
            if userid:
                #check if user exit in database
                    if GoogleTokenValidator.check_user_email_exists(email):
                        return Response({"user_state": "user already exits"}, status=status.HTTP_200_OK)
                    else:
                        user_payload = {"email": email, "username": email, "password": "pop"}
                # creat new user
                       # Create a new user without password
                    user = get_user_model().objects.filter(email=email).first()
                    if not user:
                        # Create a new user without password
                        user = get_user_model().objects.create(email=email, username=email)

                    # Ensure the user is marked as verified
                    email_address, created = EmailAddress.objects.get_or_create(
                        user=user,
                        email=email,
                        primary=True,
                        verified=True
                    )

                    # If the email address was not created, it means it already existed
                    if not created:
                        # Handle the case where the email address already existed
                        # (e.g., user already signed up with email)
                        pass

                    # Check if there's a social account associated with the user
                    social_account, created = SocialAccount.objects.get_or_create(
                        user=user,
                        provider='google',  # Set the provider according to your social authentication configuration
                        uid=userid,
                    )

                    # If the social account was not created, it means it already existed
                    if not created:
                        # Handle the case where the social account already existed
                        # (e.g., user already signed up with Google)

                    # Complete the signup process
                        complete_signup(
                            request, user, allauth_settings.EMAIL_VERIFICATION, None
                        )

                    return Response({"user_state": "user created successfully"}, status=status.HTTP_201_CREATED)
                                
            else:
                 return Response({"error": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST)
            
        except ValueError as e:
            # Invalid token
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    @staticmethod
    def check_user_email_exists(email):
        return CustomUser.objects.filter(email=email).exists()
    
    @staticmethod
    def check_user_email_verified(email):
        return CustomUser.objects.filter(email=email).is_active
    
    @staticmethod
    def get_user_with(email):
        return CustomUser.objects.filter(email=email).first()
            
