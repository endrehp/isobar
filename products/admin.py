from django.contrib import admin
#from .models import Category
from .models import Product, Purchase, Event, Comment

#admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Event)
admin.site.register(Comment)
