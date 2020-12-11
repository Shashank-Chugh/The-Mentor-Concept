from django.db import models
# Create your models here.

class Contest(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    duration=models.CharField(max_length=40)
    start_time=models.CharField(max_length=40)
    
    def __str__(self):
        return self.name 


     

    
    