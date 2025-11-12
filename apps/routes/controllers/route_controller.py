"""
Controllers (Views) for Routes app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.routes.services.route_service import RouteService
from apps.users.decorators import trekly_admin_required

route_service = RouteService()


def home_view(request):
    """Home page view."""
    routes = route_service.get_featured_routes()
    popular_routes = route_service.get_popular_routes()
    
    context = {
        'routes': routes,
        'popular_routes': popular_routes,
    }
    
    return render(request, 'routes/home.html', context)


def route_list_view(request):
    """List all routes with filters."""
    query = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')
    location = request.GET.get('location', '')
    
    routes = route_service.filter_routes(
        query=query,
        difficulty=difficulty,
        location=location
    )
    
    context = {
        'routes': routes,
        'query': query,
        'difficulty': difficulty,
        'location': location,
    }
    
    return render(request, 'routes/route_list.html', context)


def route_detail_view(request, route_id):
    """Detail view for a specific route."""
    route = route_service.get_route_by_id(route_id)
    
    if not route:
        messages.error(request, 'La ruta no existe.')
        return redirect('route_list')
    
    reviews = route.reviews.select_related('user').order_by('-created_at')
    
    context = {
        'route': route,
        'reviews': reviews,
    }
    
    return render(request, 'routes/route_detail.html', context)


@trekly_admin_required
def route_create_view(request):
    """Create a new route (only Trekly admins)."""
    if request.method == 'POST':
        route_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'difficulty': request.POST.get('difficulty'),
            'duration': request.POST.get('duration'),
            'price': request.POST.get('price'),
            'created_by': request.user,
        }
        
        image = request.FILES.get('image')
        if image:
            route_data['image'] = image
        
        route = route_service.create_route(route_data)
        
        if route:
            messages.success(request, 'Ruta creada exitosamente.')
            return redirect('route_detail', route_id=route.id)
        else:
            messages.error(request, 'Error al crear la ruta.')
    
    return render(request, 'routes/route_form.html')


@trekly_admin_required
def route_edit_view(request, route_id):
    """Edit a route (only Trekly admins)."""
    route = get_object_or_404(route_service.repository.model, id=route_id)

    if request.method == 'POST':
        route_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'location': request.POST.get('location'),
            'difficulty': request.POST.get('difficulty'),
            'duration': request.POST.get('duration'),
            'price': request.POST.get('price'),
        }
        
        image = request.FILES.get('image')
        if image:
            route_data['image'] = image
        
        updated_route = route_service.update_route(route_id, route_data)
        
        if updated_route:
            messages.success(request, 'Ruta actualizada exitosamente.')
            return redirect('route_detail', route_id=route_id)
        else:
            messages.error(request, 'Error al actualizar la ruta.')
    
    return render(request, 'routes/route_form.html', {'route': route})


@trekly_admin_required
def route_delete_view(request, route_id):
    """Delete a route (only Trekly admins)."""
    route = get_object_or_404(route_service.repository.model, id=route_id)

    if request.method == 'POST':
        if route_service.delete_route(route_id):
            messages.success(request, 'Ruta eliminada exitosamente.')
            return redirect('route_list')
        else:
            messages.error(request, 'Error al eliminar la ruta.')
    
    return render(request, 'routes/route_confirm_delete.html', {'route': route})


@trekly_admin_required
def my_routes_view(request):
    """View all routes (for Trekly admins)."""
    routes = route_service.get_all_routes()
    return render(request, 'routes/my_routes.html', {'routes': routes})
