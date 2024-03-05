from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserConsumptionSession, UserCompleteSession, UserActivitySession, Activity, Emotion, Stash, SubEmotion
from .serializers import UserConsumptionSessionSerializer, UserCompleteSessionSerializer, UserActivitySessionSerializer, ActivitySerializer, SessionFeedBackSerializer,SubEmotionSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db import DatabaseError
from .serializers import EmotionSerializer
from .models import Emotion
from rest_framework.exceptions import APIException


class UserConsumptionSessionView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserConsumptionSessionSerializer(data=request.data)
        try:
            if serializer.is_valid():
                # Check if emotion_id and stash_id are present in request data
                if 'emotion_id' not in serializer.validated_data or 'stash_id' not in serializer.validated_data:
                    data = {
                        "response": "emotion_id and stash_id are required fields"
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

                # Fetch emotion and stash objects using the provided IDs
                emotion_id = serializer.validated_data['emotion_id']
                stash_id = serializer.validated_data['stash_id']
                emotion = Emotion.objects.filter(id=emotion_id).first()
                stash = Stash.objects.filter(id=stash_id).first()

                # Check if both emotion and stash exist
                if emotion and stash: 
                    # Assign the authenticated user to the created_by field
                    serializer.validated_data['emotion_id'] = emotion.id
                    serializer.validated_data['stash_id'] = stash.id
                    #serializer.validated_data['created_by'] = request.user
                    serializer.save(created_by=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    data = {
                        "response": "emotion or stash items do not exist"
                    }
                    print("got here", serializer.errors)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {
                    "response": "error serializing request"
                }
                print(serializer.errors)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            data = {
                "response": "Database error occurred"
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    
    def perform_create(self, serializer):
        # Override this method to tie the user to the created item
        serializer.save(created_by=self.request.user)

    def get(self, request, session_id=None, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            if session_id:
                session = get_object_or_404(UserConsumptionSession, id=session_id, created_by=request.user)
                serializer = UserConsumptionSessionSerializer(session)
                return Response(serializer.data)
            else:
                sessions = UserConsumptionSession.objects.filter(created_by=request.user)
                serializer = UserConsumptionSessionSerializer(sessions, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, session_id):
        try:
            return UserConsumptionSession.objects.get(id=session_id, created_by=self.request.user)
        except UserConsumptionSession.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
        
class UserActivitySessionView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserActivitySessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        # Override this method to tie the user to the created item
        activity_id = self.request.data.get('activity_item')
        
        activity_item = self.get_activity_item_by(activity_id)  # Replace with your logic
        serializer.save(created_by=self.request.user, activity_item = activity_item)

    def get(self, request, session_id=None, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            if session_id:
                session = get_object_or_404(UserActivitySession, id=session_id, created_by=request.user)
                serializer = UserActivitySessionSerializer(session)
                return Response(serializer.data)
            else:
                sessions = UserActivitySession.objects.filter(created_by=request.user)
                serializer = UserActivitySessionSerializer(sessions, many=True)
                return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, session_id):
        try:
            return UserActivitySession.objects.get(id=session_id, created_by=self.request.user)
        except UserActivitySession.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    

    def get_activity_item_by(activity_id):
        try:
            # Query the Activity model based on the activity_id
            activity_item = Activity.objects.get(id=activity_id)
            return activity_item
        except Activity.DoesNotExist:
            # Handle the case where the Activity does not exist
            # You might want to create the Activity or raise an exception, depending on your logic
            raise Exception("Activity not found")

# Use get_activity_item_logic(request.data['activity_id']) in the perform_create method of the view

        
    


class UserCompleteSessionView(APIView):
    
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_complete_sessions = UserCompleteSession.objects.filter(created_by=request.user)
        serializer = UserCompleteSessionSerializer(user_complete_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk, format=None):
        user_complete_session = self.get_object(pk)
        serializer = UserCompleteSessionSerializer(user_complete_session)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            if not request.user.is_authenticated:
                raise APIException('Authentication credentials were not provided.', status_code=status.HTTP_401_UNAUTHORIZED)
            
            # Create a SessionFeedBack object from the request data
            feedback_serializer = SessionFeedBackSerializer(data=request.data.get('feedback'))
            if not feedback_serializer.is_valid():
                raise APIException(feedback_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
            feedback = feedback_serializer.save()

            # Create a UserCompleteSession object and assign the feedback's pk
            complete_session_data = request.data.copy()
            complete_session_data['feedback'] = feedback.pk
            user_complete_session_serializer = UserCompleteSessionSerializer(data=complete_session_data)
            if not user_complete_session_serializer.is_valid():
                raise APIException(user_complete_session_serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
            user_complete_session_serializer.save(created_by=request.user)
            return Response(user_complete_session_serializer.data, status=status.HTTP_201_CREATED)
        
        except DatabaseError:
            raise APIException('A database error occurred.', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_object(self, pk):
        try:
            return UserCompleteSession.objects.get(pk=pk)
        except UserCompleteSession.DoesNotExist:
            raise Http404


class ActivityListView(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()  # 
        


class EmotionListView(APIView):
    def get(self, request, format=None):
        emotions = Emotion.objects.all()
        serializer = EmotionSerializer(emotions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubEmotionListView(APIView):
    def get(self, request, format=None):
        sub_emotions = SubEmotion.objects.all()
        serializer = SubEmotionSerializer(sub_emotions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SubEmotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)