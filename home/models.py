from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.signals import user_logged_in, user_logged_out
import os


# ----THIS ARE THE MODELS IN THE DATABASE--------

class Group(models.Model):
    modifier = models.IntegerField(default=1)
    name = models.CharField(max_length=100, )
    creator = models.IntegerField(default=1)
    members = models.ManyToManyField(User, related_name='members')
    isLeader = models.ManyToManyField(User, related_name='isLeader')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:group_detail', kwargs={'id': self.id})

    def get_absolute_urlf(self):
        return reverse('home:group_detail_files', kwargs={'id': self.id})


class Document(models.Model):
    modifier = models.IntegerField(default=1)
    name = models.CharField(max_length=50, default="")
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)
    docfile = models.FileField(upload_to='documents', null=True)
    creator = models.IntegerField(default=1)
    time = models.DateTimeField(default=datetime.now)
    filehash = models.CharField(max_length=100, default="")

    def get_absolute_url(self):
        return reverse('home:group_detail_files', kwargs={'id': self.group.id})

    def filename(self):
        return os.path.basename(self.docfile.name)


# --REMOVE-FILE--FROM DATABASE ON DOCUMENT MODEL DELETE
@receiver(models.signals.post_delete, sender=Document)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.docfile:
        _delete_file(instance.docfile.path)


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


class GroupComment(models.Model):
    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
    hasRead = models.ManyToManyField(User)
    creator = models.CharField(max_length=50, default="")
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('home:group_detail_files', kwargs={'id': self.group.id})


class DocumentComment(models.Model):
    title = models.CharField(max_length=100)
    comment = models.CharField(max_length=500)
    creator = models.CharField(max_length=50, default="")
    hasRead = models.ManyToManyField(User)
    document = models.ForeignKey(Document, default=1, on_delete=models.CASCADE)

    def get_absolute_url(self):
        id = self.document.group.id
        return reverse('home:group_detail_files', kwargs={'id': id})


class Log(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    group = models.IntegerField(default=0)
    action = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    time = models.DateTimeField(default=datetime.now)


# ------------SIGNALS-FROM MODELS MAINLY FOR LOGGING ACTIVITY--------------------


# ---GROUPS
@receiver(models.signals.post_save, sender=Group)
def create_group(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "created/edited group"
    log.name = instance.name
    log.group = instance.id

    for u in instance.members.all():
        send_mail('File Repo Site', 'You have been added to the group: ' + instance.name, 'info@gmail.com',[u.mail])
    user = get_object_or_404(User, id=instance.modifier)
    log.user = user
    log.save()


@receiver(models.signals.pre_delete, sender=Group)
def delete_group(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted group"
    log.name = instance.name
    log.group = instance.id
    for u in instance.members.all():
        send_mail('File Repo Site', 'The group  ' + instance.name+ ' that you were a member of has been deleted.', 'info@gmail.com',[u.email])
    user = get_object_or_404(User, id=instance.modifier)
    log.user = user
    log.save()


# ---GROUP COMMENTS
@receiver(models.signals.pre_save, sender=GroupComment)
def create_group_comment(sender, instance, *args, **kwargs):
    log = Log()
    if instance in GroupComment.objects.all():
        log.action = "edited comment:"
    else:
        log.action = "added comment:"
    log.name = instance.title
    log.group = instance.group.id
    user = get_object_or_404(User, id=instance.group.modifier)
    log.user = user
    log.save()


@receiver(models.signals.post_delete, sender=GroupComment)
def delete_group_comment(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted comment:"
    log.name = instance.title
    log.group = instance.group.id
    user = get_object_or_404(User, id=instance.group.modifier)
    log.user = user
    log.save()


# ---DOCUMENTS
@receiver(models.signals.pre_save, sender=Document)
def create_document(sender, instance, *args, **kwargs):
    log = Log()
    if instance in Document.objects.all():
        log.action = "edited document:"
    else:
        log.action = "added document:"

    for u in instance.group.members.all():
        send_mail('File Repo Site', 'A document has been added to ' + instance.group.name, 'info@gmail.com',[u.email])
    log.name = instance.name
    log.group = instance.group.id
    user = get_object_or_404(User, id=instance.modifier)
    log.user = user
    log.save()


@receiver(models.signals.pre_delete, sender=Document)
def delete_document(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted document:"
    log.name = instance.name
    log.group = instance.group.id
    user = get_object_or_404(User, id=instance.modifier)
    log.user = user
    log.save()


# ---DOCUMENT COMMENTS
@receiver(models.signals.pre_save, sender=DocumentComment)
def create_document_comment(sender, instance, *args, **kwargs):
    log = Log()
    if instance in DocumentComment.objects.all():
        log.action = "edited comment to:"
    else:
        log.action = "added comment to:"
    log.name = instance.document.name
    log.group = instance.document.group.id

    user = get_object_or_404(User, id=instance.document.modifier)
    log.user = user
    log.save()


@receiver(models.signals.post_delete, sender=DocumentComment)
def delete_document_comment(sender, instance, *args, **kwargs):
    log = Log()
    log.action = "deleted comment to:"
    log.name = instance.document.name
    log.group = instance.document.group.id
    user = get_object_or_404(User, id=instance.document.modifier)
    log.user = user
    log.save()


# -----LOG-IN/OUT---
@receiver(user_logged_in)
def user_login(sender, user, request, *args, **kwargs):
    log = Log()
    log.action = "user logged in :"
    log.name = user.username
    log.user = user
    log.save()


@receiver(user_logged_out)
def user_logout(sender, user, request, *args, **kwargs):
    log = Log()
    log.action = "user logged out :"
    log.name = user.username
    log.user = user
    log.save()
