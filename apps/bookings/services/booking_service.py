"""
Booking Service - Business logic layer for Booking operations.
"""
from apps.bookings.repositories import BookingRepository
from datetime import date


class BookingService:
    """Service class for Booking business logic."""

    def __init__(self):
        self.repository = BookingRepository()

    def get_all_bookings(self):
        """Retrieve all bookings."""
        return self.repository.get_all()

    def get_booking_by_id(self, booking_id):
        """Retrieve booking by ID."""
        return self.repository.get_by_id(booking_id)

    def get_user_bookings(self, user):
        """Retrieve all bookings for a user."""
        return self.repository.get_by_user(user)

    def get_guide_bookings(self, guide):
        """Retrieve all bookings for a guide's routes."""
        return self.repository.get_guide_bookings(guide)

    def create_booking(self, booking_data):
        """
        Create a new booking.
        Validates date and calculates total price.
        """
        # Validate date is not in the past
        booking_date = booking_data.get('date')
        if booking_date < date.today():
            raise ValueError("No puedes reservar una fecha pasada")

        # Validate participants
        participants = booking_data.get('participants', 1)
        if participants < 1:
            raise ValueError("Debe haber al menos 1 participante")

        return self.repository.create(booking_data)

    def update_booking(self, booking_id, data, user):
        """Update booking information."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise ValueError("Reserva no encontrada")

        if booking.user != user and not user.is_staff:
            raise PermissionError("No tienes permiso para editar esta reserva")

        return self.repository.update(booking, data)

    def cancel_booking(self, booking_id, user):
        """Cancel a booking."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise ValueError("Reserva no encontrada")

        if booking.user != user and not user.is_staff:
            raise PermissionError("No tienes permiso para cancelar esta reserva")

        if booking.status == 'cancelled':
            raise ValueError("Esta reserva ya está cancelada")

        return self.repository.update(booking, {'status': 'cancelled'})

    def confirm_booking(self, booking_id, user):
        """Confirm a booking (guide only)."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise ValueError("Reserva no encontrada")

        if booking.route.created_by != user and not user.is_staff:
            raise PermissionError("Solo el guía puede confirmar esta reserva")

        if booking.status != 'pending':
            raise ValueError("Solo se pueden confirmar reservas pendientes")

        return self.repository.update(booking, {'status': 'confirmed'})

    def complete_booking(self, booking_id, user):
        """Mark booking as completed."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise ValueError("Reserva no encontrada")

        if booking.route.created_by != user and not user.is_staff:
            raise PermissionError("Solo el guía puede completar esta reserva")

        return self.repository.update(booking, {'status': 'completed'})

    def delete_booking(self, booking_id, user):
        """Delete a booking."""
        booking = self.repository.get_by_id(booking_id)
        if not booking:
            raise ValueError("Reserva no encontrada")

        if booking.user != user and not user.is_staff:
            raise PermissionError("No tienes permiso para eliminar esta reserva")

        self.repository.delete(booking)
