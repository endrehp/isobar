from django.contrib import admin
from django.urls import path, include
from products import views
from django.conf.urls.static import static
from django.conf import settings
#from accounts.views import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('products/', include('products.urls'), name='products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
