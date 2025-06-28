"""
URL configuration for Box Grid Habit Tracker API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, ActivityViewSet, ActivityCategoryViewSet,
    DailyGridViewSet, ActivityLogViewSet, AnalyticsViewSet,
    HealthCheckView, UserProfileViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'categories', ActivityCategoryViewSet, basename='category')
router.register(r'grids', DailyGridViewSet, basename='grid')
router.register(r'logs', ActivityLogViewSet, basename='log')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Health check endpoint
    path('health/', HealthCheckView.as_view(), name='health'),
    
    # Grid range endpoint (custom URL pattern)
    path('grids/range/<str:start_date>/<str:end_date>/', 
         DailyGridViewSet.as_view({'get': 'grid_range'}), 
         name='grid-range'),
] 