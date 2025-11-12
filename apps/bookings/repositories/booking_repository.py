"""
Booking Repository - Data access layer for Booking model.
"""
from apps.bookings.models import Booking
from django.db.models import Q


class BookingRepository:
    """Repository for Booking model database operations."""

    @staticmethod
    def get_all():
        """Get all bookings."""
        return Booking.objects.all()

    @staticmethod
    def get_by_id(booking_id):
        """Get booking by ID."""
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None

    @staticmethod
    def get_by_user(user):
        """Get all bookings for a user."""
        return Booking.objects.filter(user=user)

    @staticmethod
    def get_by_route(route):
        """Get all bookings for a route."""
        return Booking.objects.filter(route=route)

    @staticmethod
    def get_by_status(status):
        """Get bookings filtered by status."""
        return Booking.objects.filter(status=status)

    @staticmethod
    def get_pending_bookings(user):
        """Get pending bookings for a user."""
        return Booking.objects.filter(user=user, status='pending')

    @staticmethod
    def get_confirmed_bookings(user):
        """Get confirmed bookings for a user."""
        return Booking.objects.filter(user=user, status='confirmed')

    @staticmethod
    def create(booking_data):
        """Create a new booking."""
        return Booking.objects.create(**booking_data)

    @staticmethod
    def update(booking, data):
        """Update booking data."""
        for key, value in data.items():
            setattr(booking, key, value)
        booking.save()
        return booking

    @staticmethod
    def delete(booking):
        """Delete a booking."""
        booking.delete()

    @staticmethod
    def get_guide_bookings(guide):
        """Get all bookings for routes created by a guide."""
        return Booking.objects.filter(route__created_by=guide)
