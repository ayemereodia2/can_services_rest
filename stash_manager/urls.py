# urls.py
from django.urls import path
from .views import StashView

urlpatterns = [
    path('stash/', StashView.as_view(), name='stash-list'),
]
