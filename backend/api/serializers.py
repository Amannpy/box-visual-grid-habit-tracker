"""
Serializers for Box Grid Habit Tracker API.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from activities.models import Activity, ActivityCategory, DailyGrid, ActivityLog
from analytics.models import UserAnalytics, ActivityPattern, WeeklyReport

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'timezone', 'subscription_tier', 'bio', 'avatar',
            'default_grid_size', 'theme', 'email_notifications',
            'push_notifications', 'reminder_time', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class ActivityCategorySerializer(serializers.ModelSerializer):
    """Serializer for ActivityCategory model."""
    
    class Meta:
        model = ActivityCategory
        fields = ['id', 'name', 'color', 'icon', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    category = ActivityCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    completion_rate = serializers.ReadOnlyField()
    current_streak = serializers.ReadOnlyField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'color', 'icon', 'category', 'category_id',
            'description', 'is_active', 'frequency', 'target_count',
            'reminder_enabled', 'reminder_time', 'reminder_days',
            'completion_rate', 'current_streak', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        if category_id:
            try:
                validated_data['category'] = ActivityCategory.objects.get(id=category_id)
            except ActivityCategory.DoesNotExist:
                pass
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        if category_id is not None:
            if category_id:
                try:
                    validated_data['category'] = ActivityCategory.objects.get(id=category_id)
                except ActivityCategory.DoesNotExist:
                    validated_data['category'] = None
            else:
                validated_data['category'] = None
        return super().update(instance, validated_data)


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model."""
    activity = ActivitySerializer(read_only=True)
    activity_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'activity', 'activity_id', 'date', 'grid_position',
            'notes', 'logged_at'
        ]
        read_only_fields = ['id', 'logged_at']


class DailyGridSerializer(serializers.ModelSerializer):
    """Serializer for DailyGrid model."""
    activities_logged = serializers.JSONField(read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    grid_dimensions = serializers.ReadOnlyField()
    
    class Meta:
        model = DailyGrid
        fields = [
            'id', 'date', 'grid_size', 'activities_logged',
            'completion_percentage', 'grid_dimensions', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GridLogActivitySerializer(serializers.Serializer):
    """Serializer for logging activity in grid."""
    activity_id = serializers.IntegerField()
    position = serializers.IntegerField(min_value=0)
    
    def validate_position(self, value):
        user = self.context['request'].user
        grid_size = user.default_grid_size
        if value >= grid_size:
            raise serializers.ValidationError(f"Position must be less than {grid_size}")
        return value
    
    def validate_activity_id(self, value):
        user = self.context['request'].user
        try:
            Activity.objects.get(id=value, user=user, is_active=True)
        except Activity.DoesNotExist:
            raise serializers.ValidationError("Invalid activity ID")
        return value


class UserAnalyticsSerializer(serializers.ModelSerializer):
    """Serializer for UserAnalytics model."""
    
    class Meta:
        model = UserAnalytics
        fields = [
            'total_activities_logged', 'total_days_tracked',
            'longest_streak', 'current_streak', 'average_completion_rate',
            'last_activity_date', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class ActivityPatternSerializer(serializers.ModelSerializer):
    """Serializer for ActivityPattern model."""
    activity = ActivitySerializer(read_only=True)
    
    class Meta:
        model = ActivityPattern
        fields = [
            'id', 'activity', 'pattern_type', 'pattern_data',
            'confidence_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WeeklyReportSerializer(serializers.ModelSerializer):
    """Serializer for WeeklyReport model."""
    
    class Meta:
        model = WeeklyReport
        fields = [
            'id', 'week_start', 'week_end', 'total_activities',
            'completion_rate', 'streak_maintained', 'top_activities',
            'insights', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class StreakAnalyticsSerializer(serializers.Serializer):
    """Serializer for streak analytics."""
    activity_id = serializers.IntegerField()
    activity_name = serializers.CharField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    completion_rate = serializers.FloatField()


class CompletionRateSerializer(serializers.Serializer):
    """Serializer for completion rate analytics."""
    activity_id = serializers.IntegerField()
    activity_name = serializers.CharField()
    completion_rate = serializers.FloatField()
    total_logs = serializers.IntegerField()
    target_count = serializers.IntegerField()


class PatternInsightSerializer(serializers.Serializer):
    """Serializer for pattern insights."""
    pattern_type = serializers.CharField()
    pattern_data = serializers.JSONField()
    confidence_score = serializers.FloatField()
    description = serializers.CharField()


class GridRangeSerializer(serializers.Serializer):
    """Serializer for grid range data."""
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    grids = DailyGridSerializer(many=True)
    total_activities = serializers.IntegerField()
    average_completion_rate = serializers.FloatField() 