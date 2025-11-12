"""
Review Service - Business logic layer for Review operations.
"""
from apps.reviews.repositories import ReviewRepository


class ReviewService:
    """Service class for Review business logic."""

    def __init__(self):
        self.repository = ReviewRepository()

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.repository.get_all()

    def get_review_by_id(self, review_id):
        """Retrieve review by ID."""
        return self.repository.get_by_id(review_id)

    def get_route_reviews(self, route):
        """Retrieve all reviews for a route."""
        return self.repository.get_by_route(route)

    def get_user_reviews(self, user):
        """Retrieve all reviews by a user."""
        return self.repository.get_by_user(user)

    def create_review(self, review_data):
        """
        Create a new review.
        Validates user hasn't already reviewed the route.
        """
        user = review_data.get('user')
        route = review_data.get('route')

        # Check if user has already reviewed this route
        if self.repository.user_has_reviewed(user, route):
            raise ValueError("Ya has dejado una reseña para esta ruta")

        # Validate rating
        rating = review_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValueError("La calificación debe estar entre 1 y 5")

        return self.repository.create(review_data)

    def update_review(self, review_id, data, user):
        """Update review information."""
        review = self.repository.get_by_id(review_id)
        if not review:
            raise ValueError("Reseña no encontrada")

        if review.user != user and not user.is_staff:
            raise PermissionError("No tienes permiso para editar esta reseña")

        # Validate rating if being updated
        if 'rating' in data:
            rating = data['rating']
            if rating < 1 or rating > 5:
                raise ValueError("La calificación debe estar entre 1 y 5")

        return self.repository.update(review, data)

    def delete_review(self, review_id, user):
        """Delete a review."""
        review = self.repository.get_by_id(review_id)
        if not review:
            raise ValueError("Reseña no encontrada")

        if review.user != user and not user.is_staff:
            raise PermissionError("No tienes permiso para eliminar esta reseña")

        self.repository.delete(review)

    def user_can_review(self, user, route):
        """Check if user can review a route."""
        return not self.repository.user_has_reviewed(user, route)
