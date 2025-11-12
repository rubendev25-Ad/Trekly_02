"""
Services layer for Routes app.
"""
from typing import Optional, List
from apps.routes.repositories.route_repository import RouteRepository
from apps.routes.models import Route


class RouteService:
    """Service class for route business logic."""

    def __init__(self):
        self.repository = RouteRepository()

    def create_route(self, route_data: dict) -> Optional[Route]:
        """Create a new route."""
        try:
            route = self.repository.create(**route_data)
            return route
        except Exception as e:
            print(f"Error creating route: {e}")
            return None

    def get_route_by_id(self, route_id: int) -> Optional[Route]:
        """Get route by ID."""
        return self.repository.get_by_id(route_id)

    def get_all_routes(self):
        """Get all routes."""
        return self.repository.get_all()

    def get_featured_routes(self):
        """Get featured routes (active routes)."""
        return Route.objects.filter(is_active=True).order_by('-created_at')[:6]

    def get_popular_routes(self):
        """Get popular routes (most bookings)."""
        from django.db.models import Count
        return Route.objects.filter(is_active=True).annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:3]

    def get_routes_by_guide(self, guide):
        """Get routes by guide."""
        return self.repository.get_routes_by_guide(guide)

    def filter_routes(self, query='', difficulty='', location=''):
        """Filter routes by query, difficulty, and location."""
        routes = Route.objects.filter(is_active=True)
        
        if query:
            from django.db.models import Q
            routes = routes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        
        if difficulty:
            routes = routes.filter(difficulty=difficulty)
        
        if location:
            routes = routes.filter(location__icontains=location)
        
        return routes.order_by('-created_at')

    def update_route(self, route_id: int, route_data: dict) -> Optional[Route]:
        """Update route."""
        return self.repository.update(route_id, **route_data)

    def delete_route(self, route_id: int) -> bool:
        """Delete route."""
        return self.repository.delete(route_id)
