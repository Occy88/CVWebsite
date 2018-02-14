from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime
import os


class Group(models.Model):
    name=models.CharField(max_length=100,)
    creator=models.IntegerField(default=1)
    members=models.ManyToManyField(User, related_name='members')
    isLeader=models.ManyToManyField(User, related_name='isLeader')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:group_detail',kwargs={'id':self.id})
    def get_absolute_urlf(self):
        return reverse('home:group_detail_files',kwargs={'id':self.id})

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

class GroupComment(models.Model):
    title = models.CharField(max_length=100)
    comment=models.CharField(max_length=500)
    group=models.ForeignKey(Group, default=1,on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('home:group_detail_files',kwargs={'id':self.group.id})

class DocumentComment(models.Model):
    title=models.CharField(max_length=100)
    comment=models.CharField(max_length=500)
    document=models.ForeignKey(Document, default=1,on_delete=models.CASCADE)
    def get_absolute_url(self):
        id=self.document.group.id
        return reverse('home:group_detail_files',kwargs={'id':id})


#---------------LOGS-----------------
class Log(models.Model):
    user=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    action = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.now)
#---GROUPS
@receiver(models.signals.pre_save, sender=Group)
def create_group(sender, instance, *args, **kwargs):
    log = Log()
    if instance in Group.objects.all():
        log.action = "edited"
    else:
        log.action = "created"
    log.name = instance.name
    user = get_object_or_404(User, id=instance.creator)
    log.user = user
    log.save()

@receiver(models.signals.post_delete, sender=Group)
def delete_group(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted"
    log.name = instance.name
    user = get_object_or_404(User, id=instance.creator)
    log.user = user
    log.save()
#---GROUP COMMENTS
@receiver(models.signals.pre_save, sender=GroupComment)
def create_group(sender, instance, *args, **kwargs):
    log = Log()
    if instance in GroupComment.objects.all():
        log.action = "edited comment:"
    else:
        log.action = "added comment:"
    log.name = instance.title
    user = get_object_or_404(User, id=instance.group.creator)
    log.user = user
    log.save()

@receiver(models.signals.post_delete, sender=GroupComment)
def delete_group(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted comment:"
    log.name = instance.title
    user = get_object_or_404(User, id=instance.group.creator)
    log.user = user
    log.save()














