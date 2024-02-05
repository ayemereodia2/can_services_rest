from django.urls import path
from user_account.views import UserCreate, LoginView, GoogleTokenValidator

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),
# ]

urlpatterns = [
    path("users/", UserCreate.as_view(), name="user_create"),
    path("users/<str:identifier>/", UserCreate.as_view(), name="user-by-identifier"),
    path("token-auth/", LoginView.as_view()),
    path("google-token/", GoogleTokenValidator.as_view()),
]