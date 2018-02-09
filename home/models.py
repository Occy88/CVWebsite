from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse



class Group(models.Model):
    name=models.CharField(max_length=100,)
    members=models.ManyToManyField(User)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:group_detail',kwargs={'id':self.id})

class Document(models.Model):
    group=models.ForeignKey(Group,default=1,on_delete=models.CASCADE)
    docfile = models.FileField(upload_to='documents',null=True)
    def get_absolute_url(self):
        return reverse('home:group_detail_files',kwargs={'id':self.group.id})
