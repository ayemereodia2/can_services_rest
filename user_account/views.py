from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from google.auth.transport import requests
from google.oauth2 import id_token
import requests as rqs
from rest_framework.response import Response
from rest_framework import status

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
import random
from can_backend.utils import Utils
from .serializers import CustomUser, EmailSerializer
import base64
import json


from allauth.account import app_settings as allauth_settings
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialLogin
from allauth.socialaccount.providers.apple.provider import AppleProvider
from rest_framework.exceptions import APIException

from .serializers import UserSerializer

class UserCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer(data=request.data)

        data = {}
        
        if serializer_class.is_valid():
            email = serializer_class.validated_data['email'].strip().lower()
            password = serializer_class.validated_data['password'].strip().lower()
            
            if GoogleTokenValidator.check_user_email_exists(email):
                data['response'] = 'user account already exist'
                data['username'] = user.email
                return Response(data, status=status.HTTP_201_CREATED)
            
                
            user = CustomUser.objects.create_user_with_otp(email= email, password=password)
            data['response'] = 'Please, verify the OTP sent to your email'
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
        
        email = serializer.validated_data['email'].strip().lower()
        
        user = GoogleTokenValidator.get_user_with(email=email)
        print("e dey", user)
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'response': 'success'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'token': None,
                'user_id': 0,
                'email': None,
                'response': "unverified"
            }, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = GoogleTokenValidator.get_user_with(email=email)

        if user:
            if user.otp == otp and user.is_active == False:
                return self.update_user_property(user=user,new_value= True)
            else:
                print("user++", user.is_active)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'response': 'success'
                }, status=status.HTTP_200_OK)
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
                    'email': user.email,
                    'response': 'success'
                }, status=status.HTTP_200_OK)
                
            else:
                return Response({'token': '',
                                 'user_id': '',
                                 'email': '',
                                 'response': 'User not found',
                                 }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'response': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
   
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
                        return Response({
                                'token': None,
                                'user_id': 0,
                                'email': None,
                                'response': 'user already exist'
                        }, status=status.HTTP_200_OK) 
                    else:
                        print("user-load2")
                        user_payload = {"email": email, "password": "pop", "is_active": True}
                # creat new user
                       # Create a new user without password
                    user = get_user_model().objects.filter(email=email).first()
                    if not user:
                        # Create a new user without password
                        user = get_user_model().objects.create(email=email, is_active=True)

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
                        token, created = Token.objects.get_or_create(user=user)
                        print("user-load3", user)
                        return Response({
                            'token': token.key,
                            'user_id': user.pk,
                            'email': user.email,
                            'response': 'success'
                        }, status=status.HTTP_201_CREATED)
                        
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email,
                        'response': 'success'
                    }, status=status.HTTP_201_CREATED)                                
            else:
                 return Response({"response": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST)
            
        except ValueError as e:
            # Invalid token
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @staticmethod
    def check_user_email_exists(email):
        return CustomUser.objects.filter(email=email).exists()
    
    @staticmethod
    def check_user_email_verified(email):
        return CustomUser.objects.filter(email=email).is_active
    
    @staticmethod
    def get_user_with(email):
        return CustomUser.objects.filter(email=email).first()
    


class AppleLoginView(APIView):
    def posty(self, request):
        try:
            print("request", request.data)
            # Get the Apple ID token from the request
            apple_id_token = request.data.get('apple_id_token')
            print("got it", apple_id_token)
            
            if not apple_id_token:
                raise APIException('Apple ID token is missing')
            
            # Verify the Apple ID token
            provider = AppleProvider(request)
            print("provide1", provider)
            data = provider.verify_apple_id_token(apple_id_token)
            print("provide2", data)
            # Get the user's Apple ID and email address
            user_id = data['sub']
            email = data['email']
            
            # Check if the user already exists
            user = CustomUser.objects.filter(email=email).first()
            if user:
                # If the user exists, update their email address
                user.email = email
                user.save()
            else:
                # If the user doesn't exist, create a new user
                user = CustomUser.objects.create_user(email=email, password="", is_active=True)
            
            # Create a social account for the user
            social_app = SocialApp.objects.get(provider='apple')
            social_account = SocialAccount.objects.create(user=user, provider='apple', uid=user_id, extra_data={'email': email})
            social_login = SocialLogin(user=user, account=social_account)
            complete_social_login(request, social_login)
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'response': 'success'
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('error', e)
            return Response({
                'token': None,
                'user_id': 0,
                'email': None,
                'response': 'unverified'
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
    def post(self, request):
        # Get the authorization code from the request data
        id_token = request.data.get('apple_id_token')
        authorization_code = request.data.get('authorizationCode')
        user = request.data.get('user')

        print(id_token, authorization_code, user)
        if not authorization_code:
            return Response({
                'message': 'Authorization code is missing'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Perform the verification here, for example, using a custom verification method
        return self.verify_authorization_code(request, authorization_code)
            
    
            
    def verify_authorization_code(self,request, authorization_code):
       try: 
            secret = "eyJraWQiOiJYMjUyQURBVjhMIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJMQjVZTUc1VzZXIiwiaWF0IjoxNzA4ODQzNjk3LCJleHAiOjE3MjQzOTU2OTcsImF1ZCI6Imh0dHBzOi8vYXBwbGVpZC5hcHBsZS5jb20iLCJzdWIiOiJjb20uYXllbWVyZS5hcHBzLnF3YXkubW9iaWxlIn0.aGSbz1TD-E3usj8N0duHJ7KEiL9ne_fG4pRltOFijqPkzvgFSTwe1MamXSsFTm28faWOyscIDZ7ZmA84d_wjgQ"
            response = rqs.post('https://appleid.apple.com/auth/token', data={
                'grant_type': 'authorization_code',
                'client_id': 'com.ayemere.apps.qway.mobile',
                'code': authorization_code,
                'client_secret': secret,
            })
            
            
            if response.status_code == 200:
                # Extract user email and sub from the response
                response_data = response.json()
                # Extract the access token, refresh token, and ID token from the response
                access_token = response_data.get('access_token')
                refresh_token = response_data.get('refresh_token')
                id_token = response_data.get('id_token')
                
                email = self.decode_email(id_token)
                user_id = self.decode_sub(id_token)

               
                # Check if the user already exists
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    # If the user exists, update their email address
                    user.email = email
                    user.save()
                    return Response({
                'token': None,
                'user_id': 0,
                'email': None,
                'response': 'unverified'
            }, status=status.HTTP_200_OK)
                else:
                    # If the user doesn't exist, create a new user
                    user = CustomUser.objects.create_user(email=email,password="", is_active=True)
                
                # Create a social account for the user
                social_account = SocialAccount.objects.create(user=user, provider='apple', uid=user_id, extra_data={'email': email})
                social_login = SocialLogin(user=user, account=social_account)
               # complete_social_login(request, social_login)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email,
                    'response': 'success'
                }, status=status.HTTP_201_CREATED)
       except Exception as e:
            print('error', e)
            return Response({
                'token': None,
                'user_id': 0,
                'email': None,
                'response': 'unverified'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
        
    def decode_email(self, id_token):
        _, base64_encoded_payload, _ = id_token.split('.')
        decoded_payload = base64.b64decode(base64_encoded_payload + '=' * (4 - len(base64_encoded_payload) % 4))

        # Parse the payload as a JSON object
        payload_dict = json.loads(decoded_payload)

        # Extract the email and sub values
        email = payload_dict.get('email')
        return email
    
    def decode_sub(self, id_token):
        _, base64_encoded_payload, _ = id_token.split('.')
        decoded_payload = base64.b64decode(base64_encoded_payload + '=' * (4 - len(base64_encoded_payload) % 4))

        # Parse the payload as a JSON object
        payload_dict = json.loads(decoded_payload)

        # Extract the email and sub values
        sub = payload_dict.get('sub')
        return sub


            
class GoogleLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email'].strip().lower()
        
        user = GoogleTokenValidator.get_user_with(email=email)
        print("e dey", user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'response': 'success'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'token': None,
                'user_id': 0,
                'email': None,
                'response': "unverified"
            }, status=status.HTTP_200_OK)