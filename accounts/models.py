from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
#from products.models import Product, Purchase

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #kundenr = models.IntegerField(max_length=20, blank=True)
    saldo = models.IntegerField(default=0)
    poeng = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    def add_money(self, amount):
        self.saldo += amount
    
    def add_points(self, n_products):
        poeng = 0
        for i in range(n_products):
            poeng += 10 + 5*i
        self.poeng += poeng
        return poeng
    
    def get_drunkness(self, purchases):
        body_weight = 80
        gram_alc = 0
        for purchase in purchases:
            now = timezone.now()
            diff = now - purchase.time
            if diff.seconds < 21600:
                #product = Product.objects.get(id=purchase.product_id)
                #gram_alc += product.gram_alc
                gram_alc += 20
                hours_ago = diff.seconds/3600
            else:
                break
        
        if gram_alc > 0:
            drunkness = gram_alc/(body_weight*0.7) - 0.15*hours_ago
        else:
            drunkness = 0
            
        return drunkness
        
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()