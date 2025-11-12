"""
Booking Controllers - View layer for Booking operations.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.bookings.services import BookingService
from apps.routes.models import Route
from datetime import datetime


booking_service = BookingService()


@login_required
def booking_create_view(request, route_id):
    """Create a new booking for a route."""
    route = get_object_or_404(Route, id=route_id)

    if request.method == 'POST':
        booking_data = {
            'user': request.user,
            'route': route,
            'date': datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date(),
            'participants': int(request.POST.get('participants', 1)),
            'notes': request.POST.get('notes', ''),
            'status': 'pending',
        }

        try:
            booking = booking_service.create_booking(booking_data)
            messages.success(request, '¡Reserva creada exitosamente!')
            return redirect('booking_detail', booking_id=booking.id)
        except ValueError as e:
            messages.error(request, str(e))

    context = {'route': route}
    return render(request, 'bookings/booking_form.html', context)


@login_required
def booking_list_view(request):
    """List all user's bookings."""
    bookings = booking_service.get_user_bookings(request.user)
    context = {'bookings': bookings}
    return render(request, 'bookings/booking_list.html', context)


@login_required
def booking_detail_view(request, booking_id):
    """Detail view for a specific booking."""
    booking = booking_service.get_booking_by_id(booking_id)
    
    if not booking:
        messages.error(request, 'Reserva no encontrada.')
        return redirect('booking_list')

    if booking.user != request.user and booking.route.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para ver esta reserva.')
        return redirect('booking_list')

    context = {'booking': booking}
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def booking_cancel_view(request, booking_id):
    """Cancel a booking."""
    try:
        booking_service.cancel_booking(booking_id, request.user)
        messages.success(request, 'Reserva cancelada exitosamente.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('booking_list')


@login_required
def booking_confirm_view(request, booking_id):
    """Confirm a booking (guide only)."""
    try:
        booking_service.confirm_booking(booking_id, request.user)
        messages.success(request, 'Reserva confirmada exitosamente.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('guide_bookings')


@login_required
def booking_complete_view(request, booking_id):
    """Mark booking as completed (guide only)."""
    try:
        booking_service.complete_booking(booking_id, request.user)
        messages.success(request, 'Reserva marcada como completada.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('guide_bookings')


@login_required
def guide_bookings_view(request):
    """View bookings for guide's routes."""
    if not request.user.is_guide:
        messages.error(request, 'Solo los guías pueden acceder a esta página.')
        return redirect('home')

    bookings = booking_service.get_guide_bookings(request.user)
    context = {'bookings': bookings}
    return render(request, 'bookings/guide_bookings.html', context)
