"""
URL configuration for reviews app.
"""
from django.urls import path
from apps.reviews.controllers import (
    review_create_view,
    review_edit_view,
    review_delete_view,
    my_reviews_view,
)

urlpatterns = [
    path('create/<int:route_id>/', review_create_view, name='review_create'),
    path('<int:review_id>/edit/', review_edit_view, name='review_edit'),
    path('<int:review_id>/delete/', review_delete_view, name='review_delete'),
    path('my-reviews/', my_reviews_view, name='my_reviews'),
]
