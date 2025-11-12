"""
Unit tests for Route Service.
"""
from django.test import TestCase
from apps.routes.services import RouteService
from apps.users.models import User
from apps.routes.models import Route


class RouteServiceTestCase(TestCase):
    """Test cases for RouteService."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = RouteService()
        self.guide = User.objects.create_user(
            username='guide1',
            email='guide@test.com',
            password='testpass',
            is_guide=True
        )
        self.user = User.objects.create_user(
            username='user1',
            email='user@test.com',
            password='testpass'
        )
        self.route_data = {
            'title': 'Test Route',
            'description': 'A test route',
            'location': 'Test Location',
            'difficulty': 'moderate',
            'duration': 3,
            'price': 50.00,
        }

    def test_create_route_as_guide(self):
        """Test route creation by guide."""
        route = self.service.create_route(self.route_data, self.guide)
        self.assertIsNotNone(route)
        self.assertEqual(route.title, 'Test Route')
        self.assertEqual(route.created_by, self.guide)

    def test_create_route_as_non_guide(self):
        """Test that non-guides cannot create routes."""
        with self.assertRaises(ValueError):
            self.service.create_route(self.route_data, self.user)

    def test_get_route_by_id(self):
        """Test retrieving route by ID."""
        route = self.service.create_route(self.route_data, self.guide)
        retrieved = self.service.get_route_by_id(route.id)
        self.assertEqual(route.id, retrieved.id)

    def test_search_routes(self):
        """Test searching routes."""
        self.service.create_route(self.route_data, self.guide)
        results = self.service.search_routes('Test')
        self.assertGreater(results.count(), 0)
