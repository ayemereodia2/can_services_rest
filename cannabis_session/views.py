from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserConsumptionSession, UserCompleteSession, UserActivitySession, Activity
from .serializers import UserConsumptionSessionSerializer, UserCompleteSessionSerializer, UserActivitySessionSerializer, ActivitySerializer, SessionFeedBackSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404

class UserConsumptionSessionView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserConsumptionSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        # Override this method to tie the user to the created item
        serializer.save(created_by=self.request.user)

    def get(self, request, session_id=None, format=None):
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
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user_complete_sessions = UserCompleteSession.objects.filter(created_by=request.user)
        serializer = UserCompleteSessionSerializer(user_complete_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk, format=None):
        user_complete_session = self.get_object(pk)
        serializer = UserCompleteSessionSerializer(user_complete_session)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Extract feedback data from request
        feedback_data = request.data.pop('feedback', None)

        # Create UserCompleteSession instance
        user_complete_session_serializer = UserCompleteSessionSerializer(data=request.data)
        if user_complete_session_serializer.is_valid():
            user_complete_session = user_complete_session_serializer.save(created_by=request.user)

            # Create SessionFeedBack instance with the reference to UserCompleteSession
            if feedback_data:
                feedback_data['session'] = user_complete_session.id
                feedback_serializer = SessionFeedBackSerializer(data=feedback_data)
                if feedback_serializer.is_valid():
                    feedback_serializer.save()

            return Response(user_complete_session_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(user_complete_session_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()  # 