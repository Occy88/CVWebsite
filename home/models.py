from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents',blank=True)

class Group(models.Model):
    name=models.CharField(max_length=100,)

    members=models.ManyToManyField(User,through='Membership')
    def __str__(self):
        return self.name

class Membership(models.Model):
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    date_joined=models.DateField()
    invite_reason=models.CharField(max_length=128)

