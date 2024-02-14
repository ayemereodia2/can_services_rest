from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from can_backend.utils import Utils
from allauth.account.models import EmailAddress
from .models import CustomUser


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            return data
        else:
            raise serializers.ValidationError("Both email and password are required.")