from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    first_name = models.OneToOneField(User,on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')

# Create your models here.
