# serializers.py
from rest_framework import serializers
from .models import UserConsumptionSession,SessionFeedBack, Activity, UserActivitySession, UserCompleteSession
from .models import Emotion, SubEmotion
from stash_manager.serializers import StashSerializer


class UserConsumptionSessionSerializer(serializers.ModelSerializer):
    stash = StashSerializer()  # Nested serializer for the stash object
    class Meta:
        model = UserConsumptionSession
        fields = ('id', 'session_duration', 'session_quantity', 'session_state', 'added_item_to_stash',
                  'stash', 'created_by', 'emotion_id', 'pub_date')

class SessionFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionFeedBack
        fields = '__all__'
        
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'activity_name', 'activity_icon_id']
        
class UserActivitySessionSerializer(serializers.ModelSerializer):
    #activity = ActivitySerializer()
    class Meta:
        model = UserActivitySession
        fields = ('id', 'activity_duration', 'activity_state', 'activity', 'created_by', 'pub_date')
        
class UserCompleteSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompleteSession
        fields = ['consumption_by', 'activity_by', 'feedback', 'created_by', 'pub_date']
        

class SubEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEmotion
        fields = ('id', 'sub_emotion_name', 'emotion_icon_id','colorHex', 'main_emotions')

class EmotionSerializer(serializers.ModelSerializer):
    sub_emotions = SubEmotionSerializer(many=True, read_only=True)


    class Meta:
        model = Emotion
        fields = ('id', 'emotion_name', 'emotion_icon_id', 'colorHex', 'sub_emotions')