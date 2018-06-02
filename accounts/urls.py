from django.urls import path, include
from . import views 

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('my_profile', views.my_profile, name='my_profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('members', views.members, name='members'),
    path('member/<int:member_id>', views.member_profile, name='member_profile'),
    path('my_consumption', views.my_consumption, name='my_consumption'),
    path('balances', views.balances, name='balances'),
]
