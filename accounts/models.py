from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# user profile model (database)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    phone = models.IntegerField(default=0)
    file = models.FileField(upload_to='user_file', blank=True)

    def __str__(self):
        return self.user.username


# creates user profile for each new userr
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
# Create your models here.
