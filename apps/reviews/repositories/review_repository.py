"""
Review Repository - Data access layer for Review model.
"""
from apps.reviews.models import Review


class ReviewRepository:
    """Repository for Review model database operations."""

    @staticmethod
    def get_all():
        """Get all reviews."""
        return Review.objects.all()

    @staticmethod
    def get_by_id(review_id):
        """Get review by ID."""
        try:
            return Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return None

    @staticmethod
    def get_by_route(route):
        """Get all reviews for a route."""
        return Review.objects.filter(route=route)

    @staticmethod
    def get_by_user(user):
        """Get all reviews by a user."""
        return Review.objects.filter(user=user)

    @staticmethod
    def get_by_user_and_route(user, route):
        """Check if user has already reviewed a route."""
        try:
            return Review.objects.get(user=user, route=route)
        except Review.DoesNotExist:
            return None

    @staticmethod
    def create(review_data):
        """Create a new review."""
        return Review.objects.create(**review_data)

    @staticmethod
    def update(review, data):
        """Update review data."""
        for key, value in data.items():
            setattr(review, key, value)
        review.save()
        return review

    @staticmethod
    def delete(review):
        """Delete a review."""
        review.delete()

    @staticmethod
    def user_has_reviewed(user, route):
        """Check if user has already reviewed a route."""
        return Review.objects.filter(user=user, route=route).exists()
