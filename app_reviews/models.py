from django.db import models

# Create your models here.
class AppFeedBack(models.Model):
    app_experience = models.CharField(max_length = 50)
    comment = models.CharField(max_length = 255)