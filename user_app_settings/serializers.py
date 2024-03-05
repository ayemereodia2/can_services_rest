from rest_framework import serializers
from .models import DisplaySettings, AppNotification, AppLanguage, AppUseData

class DisplaySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisplaySettings
        fields = ['use_system_settings', 'light_mode_settings', 'dark_mode_settings']
        
class AppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppNotification
        fields = ['use_session_remainder', 'use_push_notification', 'use_email_notification', 'use_phone_notification']

class AppLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppLanguage
        fields = ['use_app_language']

class AppUseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUseData
        fields = ['user_app_data']