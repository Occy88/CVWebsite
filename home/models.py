from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
import os


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

    def filename(self):
        return os.path.basename(self.docfile.name)
def _delete_file(path):
   """ Deletes file from filesystem. """
   if os.path.isfile(path):
       os.remove(path)

@receiver(models.signals.post_delete, sender=Document)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.docfile:
        _delete_file(instance.docfile.path)

