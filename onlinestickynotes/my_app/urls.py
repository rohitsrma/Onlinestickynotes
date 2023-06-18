from django.contrib import admin
from django.urls import path
from my_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    
    ]