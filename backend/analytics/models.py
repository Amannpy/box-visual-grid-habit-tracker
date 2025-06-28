"""
Analytics models for tracking user patterns and insights.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAnalytics(models.Model):
    """
    User analytics and insights.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    total_activities_logged = models.IntegerField(default=0)
    total_days_tracked = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    average_completion_rate = models.FloatField(default=0.0)
    last_activity_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Analytics')
        verbose_name_plural = _('User Analytics')
    
    def __str__(self):
        return f"{self.user.username} Analytics"
    
    def update_analytics(self):
        """Update analytics based on current user data."""
        from activities.models import ActivityLog, DailyGrid
        from datetime import date, timedelta
        
        # Update total activities logged
        self.total_activities_logged = ActivityLog.objects.filter(user=self.user).count()
        
        # Update total days tracked
        self.total_days_tracked = DailyGrid.objects.filter(user=self.user).count()
        
        # Update last activity date
        last_log = ActivityLog.objects.filter(user=self.user).order_by('-date').first()
        if last_log:
            self.last_activity_date = last_log.date
        
        # Calculate streaks
        self.current_streak = self._calculate_current_streak()
        self.longest_streak = self._calculate_longest_streak()
        
        # Calculate average completion rate
        self.average_completion_rate = self._calculate_average_completion_rate()
        
        self.save()
    
    def _calculate_current_streak(self):
        """Calculate current streak of consecutive days with activity."""
        from activities.models import ActivityLog
        from datetime import date, timedelta
        
        current_date = date.today()
        streak = 0
        
        while True:
            if ActivityLog.objects.filter(user=self.user, date=current_date).exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self):
        """Calculate longest streak of consecutive days with activity."""
        from activities.models import ActivityLog
        from datetime import date, timedelta
        
        # Get all dates with activity
        activity_dates = set(
            ActivityLog.objects.filter(user=self.user)
            .values_list('date', flat=True)
            .order_by('date')
        )
        
        if not activity_dates:
            return 0
        
        longest_streak = 0
        current_streak = 0
        previous_date = None
        
        for activity_date in sorted(activity_dates):
            if previous_date is None:
                current_streak = 1
            elif (activity_date - previous_date).days == 1:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1
            
            previous_date = activity_date
        
        longest_streak = max(longest_streak, current_streak)
        return longest_streak
    
    def _calculate_average_completion_rate(self):
        """Calculate average completion rate over the last 30 days."""
        from activities.models import DailyGrid
        from datetime import date, timedelta
        
        thirty_days_ago = date.today() - timedelta(days=30)
        grids = DailyGrid.objects.filter(
            user=self.user,
            date__gte=thirty_days_ago
        )
        
        if not grids:
            return 0.0
        
        total_completion = sum(grid.completion_percentage for grid in grids)
        return total_completion / len(grids)


class ActivityPattern(models.Model):
    """
    Patterns and correlations between activities.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_patterns')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE, related_name='patterns')
    pattern_type = models.CharField(
        max_length=50,
        choices=[
            ('time_of_day', 'Time of Day'),
            ('day_of_week', 'Day of Week'),
            ('correlation', 'Activity Correlation'),
            ('trend', 'Trend Analysis'),
        ]
    )
    pattern_data = models.JSONField(default=dict)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Activity Pattern')
        verbose_name_plural = _('Activity Patterns')
        unique_together = ['user', 'activity', 'pattern_type']
        ordering = ['-confidence_score']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity.name} - {self.pattern_type}"


class WeeklyReport(models.Model):
    """
    Weekly summary reports for users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_reports')
    week_start = models.DateField()
    week_end = models.DateField()
    total_activities = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    streak_maintained = models.BooleanField(default=False)
    top_activities = models.JSONField(default=list)
    insights = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Weekly Report')
        verbose_name_plural = _('Weekly Reports')
        unique_together = ['user', 'week_start']
        ordering = ['-week_start']
    
    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"
    
    @classmethod
    def generate_weekly_report(cls, user, week_start):
        """Generate a weekly report for a user."""
        from datetime import timedelta
        from activities.models import ActivityLog, DailyGrid
        
        week_end = week_start + timedelta(days=6)
        
        # Get activities for the week
        week_logs = ActivityLog.objects.filter(
            user=user,
            date__range=[week_start, week_end]
        )
        
        # Get grids for the week
        week_grids = DailyGrid.objects.filter(
            user=user,
            date__range=[week_start, week_end]
        )
        
        # Calculate metrics
        total_activities = week_logs.count()
        
        # Calculate completion rate
        if week_grids:
            completion_rate = sum(grid.completion_percentage for grid in week_grids) / len(week_grids)
        else:
            completion_rate = 0.0
        
        # Get top activities
        activity_counts = {}
        for log in week_logs:
            activity_name = log.activity.name
            activity_counts[activity_name] = activity_counts.get(activity_name, 0) + 1
        
        top_activities = sorted(
            activity_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        # Generate insights
        insights = cls._generate_insights(user, week_start, week_end, week_logs)
        
        # Check if streak was maintained
        streak_maintained = cls._check_streak_maintained(user, week_start, week_end)
        
        # Create or update report
        report, created = cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                'week_end': week_end,
                'total_activities': total_activities,
                'completion_rate': completion_rate,
                'streak_maintained': streak_maintained,
                'top_activities': top_activities,
                'insights': insights,
            }
        )
        
        return report
    
    @classmethod
    def _generate_insights(cls, user, week_start, week_end, week_logs):
        """Generate insights for the weekly report."""
        insights = {
            'best_day': None,
            'most_productive_time': None,
            'activity_diversity': 0,
            'consistency_score': 0.0,
        }
        
        if not week_logs:
            return insights
        
        # Find best day (most activities)
        day_counts = {}
        for log in week_logs:
            day = log.date.strftime('%A')
            day_counts[day] = day_counts.get(day, 0) + 1
        
        if day_counts:
            insights['best_day'] = max(day_counts.items(), key=lambda x: x[1])[0]
        
        # Calculate activity diversity
        unique_activities = len(set(log.activity_id for log in week_logs))
        insights['activity_diversity'] = unique_activities
        
        # Calculate consistency score
        total_possible_days = 7
        days_with_activity = len(set(log.date for log in week_logs))
        insights['consistency_score'] = (days_with_activity / total_possible_days) * 100
        
        return insights
    
    @classmethod
    def _check_streak_maintained(cls, user, week_start, week_end):
        """Check if user maintained their streak during the week."""
        from activities.models import ActivityLog
        from datetime import timedelta
        
        # Check if there was activity on every day of the week
        current_date = week_start
        while current_date <= week_end:
            if not ActivityLog.objects.filter(user=user, date=current_date).exists():
                return False
            current_date += timedelta(days=1)
        
        return True 