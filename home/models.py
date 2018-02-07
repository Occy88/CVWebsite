from django.contrib.auth.models import User
from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='documents',blank=True)

class Group(models.Model):
    name=models.CharField(max_length=100,)
    members=models.ManyToManyField(User)

    def __str__(self):
        return self.name


