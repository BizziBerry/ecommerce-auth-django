from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailConfirmationToken

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'is_active', 'is_staff', 'is_verified', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_verified', 'date_joined')
    search_fields = ('email', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Персональная информация'), {'fields': ('phone_number', 'address')}),
        (('Статусы'), {'fields': ('is_active', 'is_staff', 'is_verified', 'is_superuser')}),
        (('Важные даты'), {'fields': ('last_login', 'date_joined', 'last_updated')}),
        (('Права доступа'), {'fields': ('groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_updated')

@admin.register(EmailConfirmationToken)
class EmailConfirmationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('created_at',)