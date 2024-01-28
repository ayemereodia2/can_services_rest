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


class LoginView2(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get("email")
        password = request.data.get("password")
                
        # user = authenticate(request, email=email, password=password)
        user = authenticate(username=username, password=password)
        
        if user:
            # Password is correct
            return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
        else:
            # Either user does not exist or password is incorrect
            return Response({"error": "Incorrect username or password"}, status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request, *args, **kwargs):
    #     email = request.data.get("email")
    #     password = request.data.get("password")
        
    #     user = authenticate(request, email=email, password=password)
        
    #     print("user-is",email, password)
    #     if user:
    #         return Response({"token": user.auth_token.key}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"error": "Incorrect username or password"}, status=status.HTTP_400_BAD_REQUEST)
    



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

