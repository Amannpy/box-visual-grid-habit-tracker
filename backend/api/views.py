"""
API views for Box Grid Habit Tracker.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date, timedelta

from .serializers import (
    UserSerializer, UserRegistrationSerializer, ActivitySerializer,
    ActivityCategorySerializer, DailyGridSerializer, ActivityLogSerializer,
    GridLogActivitySerializer, UserAnalyticsSerializer, ActivityPatternSerializer,
    WeeklyReportSerializer, StreakAnalyticsSerializer, CompletionRateSerializer,
    PatternInsightSerializer, GridRangeSerializer
)
from activities.models import Activity, ActivityCategory, DailyGrid, ActivityLog
from analytics.models import UserAnalytics, ActivityPattern, WeeklyReport


class AuthViewSet(viewsets.ViewSet):
    """Authentication endpoints."""
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """User registration endpoint."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserAnalytics.objects.create(user=user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """User login endpoint."""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """User logout endpoint."""
        logout(request)
        return Response({'message': 'Logout successful'})


class ActivityViewSet(viewsets.ModelViewSet):
    """Activity management endpoints."""
    
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle activity active status."""
        activity = self.get_object()
        activity.is_active = not activity.is_active
        activity.save()
        return Response({
            'message': f'Activity {"activated" if activity.is_active else "deactivated"}',
            'is_active': activity.is_active
        })
    
    @action(detail=False)
    def categories(self, request):
        """Get all activity categories."""
        categories = ActivityCategory.objects.all()
        serializer = ActivityCategorySerializer(categories, many=True)
        return Response(serializer.data)


class DailyGridViewSet(viewsets.ModelViewSet):
    """Daily grid management endpoints."""
    
    serializer_class = DailyGridSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return DailyGrid.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def log_activity(self, request, pk=None):
        """Log an activity in a specific grid position."""
        grid = self.get_object()
        serializer = GridLogActivitySerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            activity_id = serializer.validated_data['activity_id']
            position = serializer.validated_data['position']
            
            try:
                activity = Activity.objects.get(id=activity_id, user=request.user, is_active=True)
                grid.log_activity(activity, position)
                
                return Response({
                    'message': 'Activity logged successfully',
                    'grid': DailyGridSerializer(grid).data
                })
            except Activity.DoesNotExist:
                return Response({
                    'error': 'Activity not found'
                }, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsViewSet(viewsets.ViewSet):
    """Analytics endpoints."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False)
    def overview(self, request):
        """Get user analytics overview."""
        analytics, created = UserAnalytics.objects.get_or_create(user=request.user)
        analytics.update_analytics()
        
        serializer = UserAnalyticsSerializer(analytics)
        return Response(serializer.data)
    
    @action(detail=False)
    def streaks(self, request):
        """Get streak analytics for all activities."""
        activities = Activity.objects.filter(user=request.user, is_active=True)
        streak_data = []
        
        for activity in activities:
            streak_data.append({
                'activity_id': activity.id,
                'activity_name': activity.name,
                'current_streak': activity.current_streak,
                'longest_streak': activity.current_streak,
                'completion_rate': activity.completion_rate
            })
        
        serializer = StreakAnalyticsSerializer(streak_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def completion_rates(self, request):
        """Get completion rate analytics."""
        activities = Activity.objects.filter(user=request.user, is_active=True)
        completion_data = []
        
        for activity in activities:
            total_logs = activity.activity_logs.count()
            completion_data.append({
                'activity_id': activity.id,
                'activity_name': activity.name,
                'completion_rate': activity.completion_rate,
                'total_logs': total_logs,
                'target_count': activity.target_count
            })
        
        serializer = CompletionRateSerializer(completion_data, many=True)
        return Response(serializer.data)


class HealthCheckView(APIView):
    """Health check endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Return health status."""
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0'
        }) 