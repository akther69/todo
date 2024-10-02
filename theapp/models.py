from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class ToDo(models.Model):
    
    title=models.CharField(max_length=200)
    
    status=models.BooleanField(default=False)
    
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    
    created_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        
        return self.title