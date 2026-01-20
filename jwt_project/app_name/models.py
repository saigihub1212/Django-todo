from django.db import models

# Create your models here.
class MyUser(models.Model):
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100,null=False)
    title = models.TextField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    # age = models.IntegerField()

# class DoneByUser(models.Model):
    
    