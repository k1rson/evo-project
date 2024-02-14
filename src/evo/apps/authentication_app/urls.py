from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.AuthLoginPageView.as_view(), name='auth_page'), 
    path('reset-password', views.ResetPasswordPageView.as_view(), name='reset_password'), 
    path('registration', views.AuthRegistrPageView.as_view(), name='registr_page'), 
    path('logout', views.LogoutUserView.as_view(), name='logout')
]