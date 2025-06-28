"""
Activity and Grid models for Box Grid Habit Tracker.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ActivityCategory(models.Model):
    """
    Categories for organizing activities.
    """
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    icon = models.CharField(max_length=50, default='star')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Activity Category')
        verbose_name_plural = _('Activity Categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    """
    User-defined activities that can be logged in the grid.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    icon = models.CharField(max_length=50, default='star')
    category = models.ForeignKey(
        ActivityCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='activities'
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Scheduling options
    frequency = models.CharField(
        max_length=20,
        default='daily',
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('custom', 'Custom'),
        ]
    )
    target_count = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text=_('Target number of times to complete this activity')
    )
    
    # Reminder settings
    reminder_enabled = models.BooleanField(default=False)
    reminder_time = models.TimeField(null=True, blank=True)
    reminder_days = models.JSONField(default=list, blank=True)
    
    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')
        ordering = ['-created_at']
        unique_together = ['user', 'name']
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    @property
    def completion_rate(self):
        """Calculate completion rate for the last 30 days."""
        from datetime import date, timedelta
        thirty_days_ago = date.today() - timedelta(days=30)
        total_logs = self.activity_logs.filter(date__gte=thirty_days_ago).count()
        return min(100, (total_logs / 30) * 100)
    
    @property
    def current_streak(self):
        """Calculate current streak of consecutive days."""
        from datetime import date, timedelta
        
        current_date = date.today()
        streak = 0
        
        while True:
            if self.activity_logs.filter(date=current_date).exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak


class DailyGrid(models.Model):
    """
    Daily grid representation for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_grids')
    date = models.DateField()
    grid_size = models.IntegerField(
        default=16,
        validators=[MinValueValidator(4), MaxValueValidator(64)],
        help_text=_('Grid size (4x4=16, 6x6=36, 8x8=64)')
    )
    activities_logged = models.JSONField(
        default=dict,
        help_text=_('JSON mapping of grid positions to activity IDs')
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Daily Grid')
        verbose_name_plural = _('Daily Grids')
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    @property
    def grid_dimensions(self):
        """Return grid dimensions based on size."""
        if self.grid_size == 16:
            return 4, 4
        elif self.grid_size == 36:
            return 6, 6
        elif self.grid_size == 64:
            return 8, 8
        else:
            return 4, 4  # Default fallback
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage of the grid."""
        filled_positions = len(self.activities_logged)
        return min(100, (filled_positions / self.grid_size) * 100)
    
    def get_activity_at_position(self, position):
        """Get activity at a specific grid position."""
        activity_id = self.activities_logged.get(str(position))
        if activity_id:
            try:
                return Activity.objects.get(id=activity_id, user=self.user)
            except Activity.DoesNotExist:
                return None
        return None
    
    def log_activity(self, activity, position):
        """Log an activity at a specific position."""
        if not isinstance(position, int) or position < 0 or position >= self.grid_size:
            raise ValueError("Invalid grid position")
        
        self.activities_logged[str(position)] = activity.id
        self.save()
        
        # Create activity log entry
        ActivityLog.objects.create(
            user=self.user,
            activity=activity,
            date=self.date,
            grid_position=position
        )


class ActivityLog(models.Model):
    """
    Individual activity log entries.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activity_logs')
    date = models.DateField()
    grid_position = models.IntegerField()
    logged_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')
        ordering = ['-logged_at']
        unique_together = ['user', 'activity', 'date', 'grid_position']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity.name} on {self.date}"
    
    def save(self, *args, **kwargs):
        # Ensure the daily grid exists
        daily_grid, created = DailyGrid.objects.get_or_create(
            user=self.user,
            date=self.date,
            defaults={'grid_size': self.user.default_grid_size}
        )
        
        # Update the grid's activities_logged
        daily_grid.activities_logged[str(self.grid_position)] = self.activity.id
        daily_grid.save()
        
        super().save(*args, **kwargs) 