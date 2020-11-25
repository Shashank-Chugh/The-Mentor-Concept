from django.db import models
from django.contrib.auth.models import User


class CustomUser(models.Model):
    photoURL =  models.CharField(max_length=100)
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username 
    


    

