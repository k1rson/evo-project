# Generated by Django 5.0.2 on 2024-02-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0005_rename_userrolemodel_userpositionmodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpositionmodel',
            name='position_name',
            field=models.CharField(max_length=100, verbose_name='Название должности'),
        ),
    ]