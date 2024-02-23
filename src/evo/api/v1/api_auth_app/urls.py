from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('auth-user-token/', views.AuthorizationUserAPI.as_view(), name='auth_user_token_api'), 
    path('reset-password/', views.ResetPasswordUserAPI.as_view(), name='reset_password_api'), 
]