from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserPositionModel

class UserPositionAdmin(admin.ModelAdmin):
    list_display = ('position_name',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    list_display = ('username', 'email', 'is_staff', 'is_active', )
    list_filter = ('username', 'email', 'is_staff', 'is_active',)

    fieldsets = (
        ('Общие данные', {'fields': ('username', 'email', 'password', 'src_avatar', 'first_name', 'last_name', 'is_online', 'last_activity')}),
        ('Спец. информация', {'fields': ('is_verified_email', 'role', 'position_id')}),
        ('Права администратора', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_staff', 'is_verified_email'
            )}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserPositionModel, UserPositionAdmin)
