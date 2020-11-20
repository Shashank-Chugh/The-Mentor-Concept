from django.db import models
# Create your models here.

class Contest(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
     

    def __str__(self):
        return self.name 
    