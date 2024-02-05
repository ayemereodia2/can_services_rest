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



# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# import requests
from .serializers import UserSerializer

class UserCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer_class = UserSerializer(data= request.data)
        data = {}
        
        if serializer_class.is_valid():
            account = serializer_class.save()
            data['response'] = 'user account created'
            data['username'] = account.email
            return Response(data, status=status.HTTP_201_CREATED)
        data = serializer_class.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_user_by_identifier(self, identifier):
        user = get_object_or_404(User, Q(username=identifier) | Q(email=identifier))
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_by_identifier(self, request, identifier, *args, **kwargs):
        return self.get_user_by_identifier(identifier)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
   
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
        return User.objects.filter(email=email).exists()
            
        
        
        
# class UserActivationView(APIView):
#     def get(self, request, uid, token):
#         protocol = "https://" if request.is_secure() else "http://"
#         web_url = protocol + request.get_host()
#         uid = request.args["uid"]
#         uid = request.args["token"]
#         post_url = web_url + "/auth/activation/"
#         post_data = {"uid": uid, "token": token}
#         result = requests.post(post_url, data=post_data)
#         content = result.text
#         return Response(content)
    

# login_serializer = self.get_serializer(data=request.data)
#             if login_serializer.is_valid():
#                 user_serializer = UserRegistrationSerializer(user)
#                 return Response(
#                     {
#                         "access": login_serializer.validated_data["access"],
#                         "refresh": login_serializer.validated_data["refresh"],
#                         "user": user_serializer.data,
#                         "message": "Login successful",
#                     },
#                     status=status.HTTP_200_OK,
#                 )

