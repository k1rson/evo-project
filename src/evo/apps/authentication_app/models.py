from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager

class UserPositionModel(models.Model):
    position_name = models.CharField('Название должности', max_length=100)

    def __str__(self) -> str:
        return f'{self.position_name}'

    class Meta:
        verbose_name_plural = 'Должности'

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Accountant', 'Бухгалтер'), 
        ('Editor', 'Редактор'), 
        ('Admin', 'Администратор')
    ]

    username = models.CharField('Логин', db_index=True, max_length=255, unique=True)
    email = models.EmailField('Email', unique=True)
    is_verified_email = models.BooleanField('Верифицирован ли Email', default=False)
    src_avatar = models.ImageField('Аватар', upload_to='avatars/%Y-%m')
    role = models.CharField('Роль пользователя', max_length=255, choices=ROLE_CHOICES)
    position_id = models.ForeignKey(UserPositionModel, verbose_name='Должность пользователя', on_delete=models.CASCADE, null=True, related_name='users')
    last_activity = models.DateTimeField('Последняя активность (timezone)', default=timezone.now)
    is_online = models.BooleanField('Онлайн')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f'{self.username} / {self.email}'