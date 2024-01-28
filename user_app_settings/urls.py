
from django.urls import path
from .views import (
    DisplaySettingsView,
    AppNotificationView,
    AppLanguageView,
    AppUseDataView
)

urlpatterns = [
    path('display-settings/', DisplaySettingsView.as_view(), name='display-settings'),
    path('app-notification/', AppNotificationView.as_view(), name='app-notification'),
    path('app-language/', AppLanguageView.as_view(), name='app-language'),
    path('app-use-data/', AppUseDataView.as_view(), name='app-use-data'),
]