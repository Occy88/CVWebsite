import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Folder(models.Model):
    owner= models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    group = models.CharField(max_length=250)

    def __str__(self):
        return self.owner+",  "+ self.title

class Document(models.Model):
    folder=models.ForeignKey(Folder,on_delete=models.CASCADE)
    document_type=models.CharField(max_length=10)
    document_title=models.CharField(max_length=250)
    is_favorite= models.BooleanField(default=False)
    def __str__(self):
        return self.document_title+",  "+ self.document_type