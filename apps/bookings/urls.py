"""
URL configuration for bookings app.
"""
from django.urls import path
from apps.bookings.controllers import (
    booking_create_view,
    booking_list_view,
    booking_detail_view,
    booking_cancel_view,
    booking_confirm_view,
    booking_complete_view,
    guide_bookings_view,
)

urlpatterns = [
    path('', booking_list_view, name='booking_list'),
    path('create/<int:route_id>/', booking_create_view, name='booking_create'),
    path('<int:booking_id>/', booking_detail_view, name='booking_detail'),
    path('<int:booking_id>/cancel/', booking_cancel_view, name='booking_cancel'),
    path('<int:booking_id>/confirm/', booking_confirm_view, name='booking_confirm'),
    path('<int:booking_id>/complete/', booking_complete_view, name='booking_complete'),
    path('guide/', guide_bookings_view, name='guide_bookings'),
]
