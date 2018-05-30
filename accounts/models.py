from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #kundenr = models.IntegerField(max_length=20, blank=True)
    saldo = models.IntegerField(default=0)
    poeng = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    def add_money(self, amount):
        self.saldo += amount
        
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()