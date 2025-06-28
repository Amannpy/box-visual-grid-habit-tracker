"""
User models for Box Grid Habit Tracker.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model with additional fields for habit tracking.
    """
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text=_('User timezone for proper date handling')
    )
    subscription_tier = models.CharField(
        max_length=20,
        default='free',
        choices=[
            ('free', 'Free'),
            ('premium', 'Premium'),
            ('pro', 'Pro'),
        ],
        help_text=_('User subscription tier')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Profile fields
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Preferences
    default_grid_size = models.IntegerField(
        default=16,
        help_text=_('Default grid size (4x4=16, 6x6=36, 8x8=64)')
    )
    theme = models.CharField(
        max_length=20,
        default='light',
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto'),
        ]
    )
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    reminder_time = models.TimeField(default='09:00')
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def get_grid_size_dimensions(self):
        """Return grid dimensions based on size."""
        size = self.default_grid_size
        if size == 16:
            return 4, 4
        elif size == 36:
            return 6, 6
        elif size == 64:
            return 8, 8
        else:
            return 4, 4  # Default fallback 