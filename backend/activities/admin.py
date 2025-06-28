"""
Admin configuration for Activity models.
"""

from django.contrib import admin
from .models import ActivityCategory, Activity, DailyGrid, ActivityLog


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for ActivityCategory model."""
    
    list_display = ('name', 'color', 'icon', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model."""
    
    list_display = ('name', 'user', 'category', 'color', 'is_active', 'frequency', 'created_at')
    list_filter = ('is_active', 'frequency', 'category', 'created_at', 'reminder_enabled')
    search_fields = ('name', 'user__username', 'user__email', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'description', 'is_active')
        }),
        ('Appearance', {
            'fields': ('color', 'icon', 'category')
        }),
        ('Scheduling', {
            'fields': ('frequency', 'target_count')
        }),
        ('Reminders', {
            'fields': ('reminder_enabled', 'reminder_time', 'reminder_days')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DailyGrid)
class DailyGridAdmin(admin.ModelAdmin):
    """Admin configuration for DailyGrid model."""
    
    list_display = ('user', 'date', 'grid_size', 'completion_percentage', 'created_at')
    list_filter = ('date', 'grid_size', 'created_at')
    search_fields = ('user__username', 'user__email', 'notes')
    ordering = ('-date',)
    readonly_fields = ('created_at', 'updated_at', 'completion_percentage')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'grid_size')
        }),
        ('Content', {
            'fields': ('activities_logged', 'notes')
        }),
        ('Statistics', {
            'fields': ('completion_percentage',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Admin configuration for ActivityLog model."""
    
    list_display = ('user', 'activity', 'date', 'grid_position', 'logged_at')
    list_filter = ('date', 'logged_at', 'activity__category')
    search_fields = ('user__username', 'activity__name', 'notes')
    ordering = ('-logged_at',)
    readonly_fields = ('logged_at',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'activity', 'date', 'grid_position')
        }),
        ('Additional Info', {
            'fields': ('notes', 'logged_at')
        }),
    ) 