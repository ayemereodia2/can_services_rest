from django.db import models
from user_account.models import CustomUser
from stash_manager.models import Stash

# Create your models here.

    
class UserConsumptionSession(models.Model):
    session_duration = models.CharField(max_length = 50)
    session_quantity = models.CharField(max_length = 50)
    session_state = models.CharField(max_length = 50)
    added_item_to_stash = models.BooleanField()
    stash_id = models.CharField(max_length = 50)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    
    
class Emotion(models.Model):
    emotion_name = models.CharField(max_length = 50)
    emotion_icon_id = models.CharField(max_length = 100)
    user_consumption_session = models.ForeignKey(UserConsumptionSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.emotion_name
    

class SubEmotion(models.Model):
    sub_emotion_name = models.CharField(max_length = 50)
    emotion_icon_id = models.CharField(max_length = 100)
    main_emotions = models.ForeignKey(Emotion, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.sub_emotion_name
    

class Activity(models.Model):
    activity_name = models.CharField(max_length = 50)
    activity_icon_id = models.CharField(max_length = 100)
    def __str__(self):
        return self.activity_name

class UserActivitySession(models.Model):
    activity_duration = models.CharField(max_length = 50)
    activity_state = models.CharField(max_length = 50)
    activity_item = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    
class SessionFeedBack(models.Model):
    rating = models.CharField(max_length = 10)
    feeling = models.CharField(max_length = 20)
    optional_notes = models.CharField(max_length = 50)


# TO DO: Complete Session completion relationship.
class UserCompleteSession(models.Model):
    consumption_by = models.OneToOneField(UserConsumptionSession, on_delete=models.CASCADE)
    activity_by = models.OneToOneField(UserActivitySession, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.OneToOneField(SessionFeedBack, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    
