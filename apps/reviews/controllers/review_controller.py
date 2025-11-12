"""
Review Controllers - View layer for Review operations.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.reviews.services import ReviewService
from apps.routes.models import Route


review_service = ReviewService()


@login_required
def review_create_view(request, route_id):
    """Create a new review for a route."""
    route = get_object_or_404(Route, id=route_id)

    if not review_service.user_can_review(request.user, route):
        messages.error(request, 'Ya has dejado una reseña para esta ruta.')
        return redirect('route_detail', route_id=route_id)

    if request.method == 'POST':
        review_data = {
            'user': request.user,
            'route': route,
            'rating': int(request.POST.get('rating')),
            'comment': request.POST.get('comment'),
        }

        try:
            review_service.create_review(review_data)
            messages.success(request, '¡Reseña publicada exitosamente!')
            return redirect('route_detail', route_id=route_id)
        except ValueError as e:
            messages.error(request, str(e))

    context = {'route': route}
    return render(request, 'reviews/review_form.html', context)


@login_required
def review_edit_view(request, review_id):
    """Edit an existing review."""
    review = get_object_or_404(review_service.get_review_by_id(review_id))

    if review.user != request.user and not request.user.is_staff:
        messages.error(request, 'No tienes permiso para editar esta reseña.')
        return redirect('route_detail', route_id=review.route.id)

    if request.method == 'POST':
        data = {
            'rating': int(request.POST.get('rating')),
            'comment': request.POST.get('comment'),
        }

        try:
            review_service.update_review(review_id, data, request.user)
            messages.success(request, 'Reseña actualizada exitosamente.')
            return redirect('route_detail', route_id=review.route.id)
        except (ValueError, PermissionError) as e:
            messages.error(request, str(e))

    context = {'review': review}
    return render(request, 'reviews/review_form.html', context)


@login_required
def review_delete_view(request, review_id):
    """Delete a review."""
    review = review_service.get_review_by_id(review_id)
    
    if not review:
        messages.error(request, 'Reseña no encontrada.')
        return redirect('home')

    route_id = review.route.id

    try:
        review_service.delete_review(review_id, request.user)
        messages.success(request, 'Reseña eliminada exitosamente.')
    except (ValueError, PermissionError) as e:
        messages.error(request, str(e))
    
    return redirect('route_detail', route_id=route_id)


@login_required
def my_reviews_view(request):
    """View user's reviews."""
    reviews = review_service.get_user_reviews(request.user)
    context = {'reviews': reviews}
    return render(request, 'reviews/my_reviews.html', context)
