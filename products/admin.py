from django.contrib import admin
#from .models import Category
from .models import Product
from .models import Purchase
from .models import Event

#admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Event)
