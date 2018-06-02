from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile



class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    #category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default='udefinert3')
    #votes_total = models.IntegerField(default=1)
    image = models.ImageField(upload_to='product_images/')
    body = models.TextField(default='')
    #ForeignKey points to another object, here it points to the model User.
    #on_delete=models.CASCADE means that if we delete the user, the model product will also be deleted.
    
    def __str__(self):
        return self.title
    

    
class Purchase(models.Model):
    user = models.CharField(max_length=100, default='none')
    #customer_id = models.IntegerField(default=0)
    product = models.CharField(max_length=100, default='0')
    amount = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now())
    event = models.CharField(max_length=100, default='Enkeltsalg')
    
    
class Event(models.Model):
    title = models.CharField(max_length=200, default='Enkeltsalg')
    start_date = models.DateTimeField(default=timezone.now())
    active = models.BooleanField(default=False)
    #participants = 
    
    def __str__(self):
        return self.title + ':    ' + str(self.active)
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, default='none')
    text = models.TextField(default='')
    date = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.product.title + ' ' + self.author
    

