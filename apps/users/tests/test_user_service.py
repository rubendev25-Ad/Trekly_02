"""
Unit tests for User Service.
"""
from django.test import TestCase
from apps.users.services import UserService
from apps.users.models import User


class UserServiceTestCase(TestCase):
    """Test cases for UserService."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_register_user(self):
        """Test user registration."""
        user = self.service.register_user(self.user_data)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')

    def test_register_duplicate_username(self):
        """Test registration with duplicate username."""
        self.service.register_user(self.user_data)
        with self.assertRaises(ValueError):
            self.service.register_user(self.user_data)

    def test_get_user_by_id(self):
        """Test getting user by ID."""
        user = self.service.register_user(self.user_data)
        retrieved_user = self.service.get_user_by_id(user.id)
        self.assertEqual(user.id, retrieved_user.id)

    def test_promote_to_guide(self):
        """Test promoting user to guide."""
        user = self.service.register_user(self.user_data)
        self.assertFalse(user.is_guide)
        updated_user = self.service.promote_to_guide(user.id)
        self.assertTrue(updated_user.is_guide)

    def test_get_guides(self):
        """Test retrieving all guides."""
        user_data = self.user_data.copy()
        user_data['is_guide'] = True
        self.service.register_user(user_data)
        guides = self.service.get_guides()
        self.assertEqual(guides.count(), 1)
