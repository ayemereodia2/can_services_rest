from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AppNotification
from .serializers import AppNotificationSerializer
from .models import AppLanguage
from .serializers import AppLanguageSerializer, DisplaySettingsSerializer
from .models import AppUseData, DisplaySettings
from .serializers import AppUseDataSerializer
from rest_framework import permissions

# Create your views here.

class AppNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        notification_settings = AppNotification.objects.filter(created_by=request.user).first()
        serializer = AppNotificationSerializer(notification_settings)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        notification_settings = AppNotification.objects.filter(created_by=request.user).first()
        if notification_settings:
            serializer = AppNotificationSerializer(notification_settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "AppNotification settings not found for the user"}, status=status.HTTP_404_NOT_FOUND)
        

    
class AppLanguageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        language_settings = AppLanguage.objects.filter(created_by=request.user).first()
        serializer = AppLanguageSerializer(language_settings)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppLanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AppUseDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        app_data_settings = AppUseData.objects.filter(created_by=request.user).first()
        serializer = AppUseDataSerializer(app_data_settings)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppUseDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class DisplaySettingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        display_settings = DisplaySettings.objects.filter(created_by=request.user).first()
        serializer = DisplaySettingsSerializer(display_settings)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DisplaySettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        notification_settings = DisplaySettings.objects.filter(created_by=request.user).first()
        if notification_settings:
            serializer = DisplaySettingsSerializer(notification_settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Display settings not found for the user"}, status=status.HTTP_404_NOT_FOUND)