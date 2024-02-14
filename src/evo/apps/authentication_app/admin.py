from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)

    fieldsets = (
        ('Общие данные', {'fields': ('username', 'email', 'password', 'src_avatar', 'is_verified_email')}),
        ('Права администратора', {'fields': ('is_staff', 'is_active')}),
        ('Группы и права доступа', {'fields': ('role', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_staff', 'is_verified_email',
                'is_active', 'role', 'user_permissions'
            )}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
