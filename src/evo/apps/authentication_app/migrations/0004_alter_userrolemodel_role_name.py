# Generated by Django 5.0.2 on 2024-02-17 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0003_alter_userrolemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrolemodel',
            name='role_name',
            field=models.CharField(max_length=100, verbose_name='Название роли'),
        ),
    ]
