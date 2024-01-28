from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DisplaySettings(models.Model):
    use_system_settings = models.BooleanField()
    light_mode_settings = models.BooleanField()
    dark_mode_settings = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    

class AppNotification(models.Model):
    use_session_remainder = models.BooleanField()
    use_push_notification = models.BooleanField()
    use_email_notification = models.BooleanField()
    use_phone_notification = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class AppLanguage(models.Model):
    use_app_language = models.CharField(max_length = 100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    

class AppUseData(models.Model):
    user_app_data = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
