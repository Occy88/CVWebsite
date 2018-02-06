from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents',blank=True)

class Group(models.Model):
    leader= models.IntegerField(default=User.pk)