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
    path('quit_event', views.quit_event, name='quit_event'),
    path('select_history', views.select_history, name='select_history'),
    path('history/<int:event_id>', views.event_history, name='event_history'),
    path('history/member/<int:member_id>', views.member_history, name='member_history'),
]

