from django.shortcuts import render
from rest_framework import permissions

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Stash
from .serializers import StashSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


class StashView(APIView):

    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None):
        print("who",request)
        try:
            stashes = Stash.objects.filter(created_by=request.user)
            serializer = StashSerializer(stashes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the error if needed
            print(f"An error occurred: {e}")
            return Response({"detail": "An error occurred while fetching data from the database."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, serializer):
        # Override this method to tie the user to the created item
        serializer.save(created_by=self.request.user)
        
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        # Your view logic here...
        serializer = StashSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, stash_id, format=None):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            stash = Stash.objects.get(id=stash_id, created_by=request.user)
        except Stash.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        stash.delete()
        return Response("deleted successfully", status=status.HTTP_204_NO_CONTENT)
    