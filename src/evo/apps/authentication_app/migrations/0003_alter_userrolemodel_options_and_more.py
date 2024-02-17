# Generated by Django 5.0.2 on 2024-02-17 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_userrolemodel_customuser_роль_пользователя'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userrolemodel',
            options={'verbose_name': 'Роль пользователя', 'verbose_name_plural': 'Роли пользователей'},
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='Роль пользователя',
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='authentication_app.userrolemodel', verbose_name='Роль пользователя'),
        ),
        migrations.AlterField(
            model_name='userrolemodel',
            name='role_name',
            field=models.CharField(max_length=100, verbose_name='Роль пользователя'),
        ),
    ]
