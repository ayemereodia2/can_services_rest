# urls.py
from django.urls import path
from .views import UserConsumptionSessionView,UserActivitySessionView, UserCompleteSessionView, ActivityListView,EmotionListView,SubEmotionListView

urlpatterns = [
    path('create-consumption-session/', UserConsumptionSessionView.as_view(), name='create_consumption_session'),
    path('create-activity-session/', UserActivitySessionView.as_view(), name='create_activity_session'),

    path('user-consumption-sessions/', UserConsumptionSessionView.as_view(), name='user-consumption-session-list'),
    path('user-consumption-sessions/<int:session_id>/', UserConsumptionSessionView.as_view(), name='user-consumption-session-detail'),
    
    path('user-complete-sessions/', UserCompleteSessionView.as_view(), name='user-complete-session-list'),
    path('user-complete-sessions/<int:pk>/', UserCompleteSessionView.as_view(), name='user-complete-session-detail'),
    
    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('emotions', EmotionListView.as_view()),
    # path('sub-emotions', SubEmotionListView.as_view()),
    # Add other URLs as needed
]