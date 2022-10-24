from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('voter/login/',loginView,name='login'),
    path('voter/logout/',logoutView,name='logout'),
    path('voter/register/',register,name='register'),
    path('voter/profile/',profileView,name='profile'),
    path('otp/',otp,name='otp')
]