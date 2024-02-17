from django.db import models
from user_account.models import CustomUser

# Create your models here.

class Stash(models.Model):
    stash_name = models.CharField(max_length = 120)
    thc = models.CharField(max_length = 50)
    cbd = models.CharField(max_length = 50)
    indica = models.CharField(max_length = 50)
    strain_type = models.CharField(max_length = 100)
    strain_flavour = models.CharField(max_length = 100)
    consumption_method =  models.CharField(max_length = 100)
    total_quantity =  models.CharField(max_length = 50)
    stash_image_id =  models.CharField(max_length = 100)
    created_date = models.DateTimeField(auto_now=True)
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.stash_name
