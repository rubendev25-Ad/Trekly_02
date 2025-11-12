"""
Repository layer for Users app.
"""
from typing import Optional, List
from apps.users.models import User


class UserRepository:
    """Repository class for User model database operations."""

    def create(self, **kwargs) -> User:
        """
        Create a new user with hashed password.

        Args:
            **kwargs: User fields (username, email, password, first_name, last_name, etc.)

        Returns:
            User: The created user object
        """
        password = kwargs.pop('password', None)
        user = User.objects.create(**kwargs)
        if password:
            user.set_password(password)
            user.save()
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User's ID

        Returns:
            User: User object or None
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            username: User's username

        Returns:
            User: User object or None
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: User's email

        Returns:
            User: User object or None
        """
        try:
            return User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None

    def get_all(self) -> List[User]:
        """
        Get all users.

        Returns:
            List of User objects
        """
        return list(User.objects.all())

    def get_guides(self) -> List[User]:
        """
        Get all guides.

        Returns:
            List of User objects who are guides
        """
        return list(User.objects.filter(is_guide=True))

    def exists_by_username(self, username: str) -> bool:
        """
        Check if a user with the given username exists.

        Args:
            username: User's username

        Returns:
            bool: True if user exists, False otherwise
        """
        return User.objects.filter(username=username).exists()

    def exists_by_email(self, email: str) -> bool:
        """
        Check if a user with the given email exists.

        Args:
            email: User's email

        Returns:
            bool: True if user exists, False otherwise
        """
        return User.objects.filter(email__iexact=email).exists()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        """
        Update user.

        Args:
            user_id: User's ID
            **kwargs: Fields to update

        Returns:
            User: Updated user object or None
        """
        try:
            user = User.objects.get(id=user_id)
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
            return user
        except User.DoesNotExist:
            return None

    def delete(self, user_id: int) -> bool:
        """
        Delete user.

        Args:
            user_id: User's ID

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
