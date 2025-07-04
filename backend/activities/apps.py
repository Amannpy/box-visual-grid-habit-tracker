"""
App configuration for activities app.
"""

from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activities'
    verbose_name = 'Activities' 