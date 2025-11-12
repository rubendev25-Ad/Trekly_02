"""
Services layer for Users app.
"""
from typing import Optional, List
from apps.users.repositories.user_repository import UserRepository
from apps.users.models import User
from django.contrib.auth.hashers import make_password


class UserService:
    """Service class for User business logic."""

    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        """Retrieve all users."""
        return self.repository.get_all()

    def get_user_by_id(self, user_id):
        """Retrieve user by ID."""
        return self.repository.get_by_id(user_id)

    def get_user_by_username(self, username):
        """Retrieve user by username."""
        return self.repository.get_by_username(username)

    def get_guides(self):
        """Retrieve all guides."""
        return self.repository.get_guides()

    def register_user(self, user_data):
        """
        Register a new user.
        Validates uniqueness and creates user with hashed password.
        """
        # Validate username uniqueness
        if self.repository.exists_by_username(user_data.get('username')):
            raise ValueError("El nombre de usuario ya existe")

        # Validate email uniqueness
        if self.repository.exists_by_email(user_data.get('email')):
            raise ValueError("El correo electrónico ya está registrado")

        # Hash password
        if 'password' in user_data:
            user_data['password'] = make_password(user_data['password'])

        return self.repository.create(user_data)

    def create_user(self, user_data: dict) -> Optional[User]:
        """
        Create a new user.
        
        Args:
            user_data: Dictionary containing user data
            
        Returns:
            User: The created user object or None if failed
        """
        try:
            # Check if email already exists (case insensitive)
            email = user_data.get('email', '').lower()
            if User.objects.filter(email__iexact=email).exists():
                print(f"Email already exists: {email}")
                return None
            
            # Normalize email to lowercase
            user_data['email'] = email
            
            user = self.repository.create(**user_data)
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            import traceback
            traceback.print_exc()
            return None

    def update_user(self, user_id, data):
        """Update user information."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        # Hash password if being updated
        if 'password' in data:
            data['password'] = make_password(data['password'])

        return self.repository.update(user, data)

    def delete_user(self, user_id):
        """Delete a user."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        self.repository.delete(user)

    def promote_to_guide(self, user_id):
        """Promote user to guide status."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return self.repository.update(user, {'is_guide': True})
