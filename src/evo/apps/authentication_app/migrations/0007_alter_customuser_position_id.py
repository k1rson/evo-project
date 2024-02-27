# Generated by Django 5.0.2 on 2024-02-17 19:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0006_alter_userpositionmodel_position_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='position_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='authentication_app.userpositionmodel', verbose_name='Должность пользователя'),
        ),
    ]