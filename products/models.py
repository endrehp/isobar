from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile


'''
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)    #enforcing that there can not be two
        verbose_name_plural = "categories"       #categories under a parent with same 
                                                 #slug 

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.name]                  # post.  use __unicode__ in place of
                                                 # __str__ if you are using python 2
        k = self.parent                          

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
'''

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
    event = models.CharField(max_length=100, default='enkeltsalg')
    
    
class Event(models.Model):
    title = models.CharField(max_length=200, default='enkeltsalg')
    start_date = models.DateTimeField(default=timezone.now())
    #participants = 
    
    
