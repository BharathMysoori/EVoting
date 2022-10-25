from email.policy import default
from tokenize import blank_re
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
wards = (
	("Ward1", "Ward1"),
	("Ward2", "Ward2"),
	("Ward3", "Ward3"),
	("Ward4", "Ward4"),
	
)


class voter(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(blank=True,null=True)
    ward = models.CharField(max_length=20,choices=wards,blank=True,default='Unknown',null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    dp  = models.ImageField(blank=True,null=True,default='voterImgs/default.png',upload_to='voterImgs/')
    otp = models.CharField(max_length=6,null=True,blank=True)
    voted  = models.BooleanField(null=True,default=False)
    votedTo = models.CharField(null=True,blank=True,max_length=15)
    verified = models.BooleanField(null=True,default=False)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        voter.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance,created, **kwargs):
    if created==False:
        instance.voter.save()
        print('save-user_profile')


class candidate(models.Model):
    candiname = models.CharField(max_length=45)
    logo = models.ImageField(blank=True,null=True,upload_to='candidateLogo/')
    ward = models.CharField(max_length=45,choices=wards,blank=True,default='Unknown',null=True)
    def __str__(self):
        return self.candiname 



