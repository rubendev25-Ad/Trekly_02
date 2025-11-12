"""
Route Repository - Data access layer for Route model.
"""
from django.db import models as django_models
from apps.routes.models import Route


class RouteRepository:
    """Repository for Route model database operations."""

    @staticmethod
    def get_all():
        """Get all routes."""
        return Route.objects.filter(is_active=True)

    @staticmethod
    def get_by_id(route_id):
        """Get route by ID."""
        try:
            return Route.objects.get(id=route_id, is_active=True)
        except Route.DoesNotExist:
            return None

    @staticmethod
    def get_by_user(user):
        """Get all routes created by a user."""
        return Route.objects.filter(created_by=user, is_active=True)

    @staticmethod
    def get_by_difficulty(difficulty):
        """Get routes filtered by difficulty."""
        return Route.objects.filter(difficulty=difficulty, is_active=True)

    @staticmethod
    def get_by_location(location):
        """Get routes filtered by location."""
        return Route.objects.filter(location__icontains=location, is_active=True)

    @staticmethod
    def search(query):
        """Search routes by title, description or location."""
        return Route.objects.filter(
            is_active=True
        ).filter(
            django_models.Q(title__icontains=query) |
            django_models.Q(description__icontains=query) |
            django_models.Q(location__icontains=query)
        )

    @staticmethod
    def create(route_data):
        """Create a new route."""
        return Route.objects.create(**route_data)

    @staticmethod
    def update(route, data):
        """Update route data."""
        for key, value in data.items():
            setattr(route, key, value)
        route.save()
        return route

    @staticmethod
    def delete(route):
        """Soft delete a route."""
        route.is_active = False
        route.save()

    @staticmethod
    def get_popular_routes(limit=5):
        """Get most popular routes by bookings count."""
        from django.db.models import Count
        return Route.objects.filter(is_active=True).annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:limit]
