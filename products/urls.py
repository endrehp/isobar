from django.urls import path, include
from . import views 

urlpatterns = [
    path('menu',views.menu, name='menu'),
    path('create_product', views.create_product, name='create_product'),
    path('<int:product_id>', views.product_info, name='product_info'),
    path('start_event', views.start_event, name='start_event'),
    path('event', views.event, name='event'),
    path('payment', views.payment, name='payment'),
    path('history', views.history, name='history'),
]
