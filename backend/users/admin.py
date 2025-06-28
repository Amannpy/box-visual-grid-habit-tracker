"""
Admin configuration for User models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = ('username', 'email', 'full_name', 'subscription_tier', 'is_active', 'created_at')
    list_filter = ('subscription_tier', 'is_active', 'is_staff', 'created_at', 'theme')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'avatar')
        }),
        (_('Preferences'), {
            'fields': ('timezone', 'default_grid_size', 'theme')
        }),
        (_('Notifications'), {
            'fields': ('email_notifications', 'push_notifications', 'reminder_time')
        }),
        (_('Subscription'), {
            'fields': ('subscription_tier',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at') 