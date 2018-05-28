from django.contrib import admin
from django.urls import path, include
from products import views
#from accounts.views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('menu/',views.menu, name='menu'),
    path('accounts/', include('accounts.urls'), name='accounts'),
]
