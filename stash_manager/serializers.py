from rest_framework import serializers
from .models import Stash

class StashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stash
        fields = '__all__'
