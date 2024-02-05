from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from allauth.account.models import EmailAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data.get('username', email)

        user = User.objects.create(
            email=email,
            username=username,
        )
        user.set_password(validated_data['password'])
        user.save()

        # Send email verification
        EmailAddress.objects.create(
            user=user,
            email=email,
            primary=True,
            verified=False  # The email address is initially set as unverified
        )

        return user