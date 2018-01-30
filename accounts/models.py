from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city= models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    phone= models.IntegerField(default=0)
# Create your models here.
