from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    ROLE_CHOICES ={
        'Accountant': 'Бухгалтер', 
        'Editor': 'Редактор', 
        'Admin': 'Администратор'
    }

    username = models.CharField('Логин', db_index=True, max_length=255, unique=True)
    email = models.EmailField('Email', unique=True)
    is_verified_email = models.BooleanField('Верифицирован ли Email', default=False)
    src_avatar = models.ImageField('Аватар', upload_to='avatars/%Y-%m')
    role = models.CharField('Роль пользователя', choices=ROLE_CHOICES)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
