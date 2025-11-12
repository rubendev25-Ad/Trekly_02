"""
Custom admin controllers for Trekly.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import datetime, timedelta
from apps.users.models import User
from apps.users.decorators import admin_required
from apps.routes.models import Route


@login_required
@admin_required
def admin_dashboard(request):
    """Dashboard principal del admin de Trekly"""
    total_users = User.objects.count()
    total_guides = User.objects.filter(is_guide=True).count()
    total_admins = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Estadísticas de rutas
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(is_active=True).count()
    
    context = {
        'total_users': total_users,
        'total_guides': total_guides,
        'total_admins': total_admins,
        'active_users': active_users,
        'total_routes': total_routes,
        'active_routes': active_routes,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@admin_required
def admin_users_list(request):
    """Lista de todos los usuarios"""
    users = User.objects.all().order_by('-date_joined')
    
    # Filtros
    user_type = request.GET.get('type')
    if user_type == 'guides':
        users = users.filter(is_guide=True)
    elif user_type == 'admins':
        users = users.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif user_type == 'regular':
        users = users.filter(is_guide=False, is_staff=False, is_superuser=False)
    
    context = {
        'users': users,
        'user_type': user_type,
    }
    return render(request, 'admin/users_list.html', context)


@login_required
@admin_required
def admin_user_detail(request, user_id):
    """Detalle de un usuario específico"""
    user = get_object_or_404(User, id=user_id)
    
    context = {
        'user_detail': user,
    }
    return render(request, 'admin/user_detail.html', context)


@login_required
@admin_required
def admin_user_edit(request, user_id):
    """Editar un usuario"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Actualizar permisos
        user.is_guide = request.POST.get('is_guide') == 'on'
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_superuser = request.POST.get('is_superuser') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        
        user.save()
        messages.success(request, f'Usuario {user.username} actualizado correctamente.')
        return redirect('trekly_admin_user_detail', user_id=user.id)
    
    context = {
        'user_detail': user,
    }
    return render(request, 'admin/user_edit.html', context)


@login_required
@admin_required
def admin_stats(request):
    """Estadísticas generales del sistema"""
    # Estadísticas de usuarios
    total_users = User.objects.count()
    new_users_month = User.objects.filter(
        date_joined__gte=datetime.now() - timedelta(days=30)
    ).count()
    
    # Top guías por tours (cuando exista la app tours)
    top_guides = User.objects.filter(is_guide=True).order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'new_users_month': new_users_month,
        'top_guides': top_guides,
    }
    return render(request, 'admin/stats.html', context)


@login_required
@admin_required
def admin_routes_list(request):
    """Lista de todas las rutas"""
    routes = Route.objects.all().select_related('created_by').order_by('-created_at')
    
    # Filtros
    status = request.GET.get('status')
    if status == 'active':
        routes = routes.filter(is_active=True)
    elif status == 'inactive':
        routes = routes.filter(is_active=False)
    
    context = {
        'routes': routes,
        'status': status,
    }
    return render(request, 'admin/routes_list.html', context)


@login_required
@admin_required
def admin_route_detail(request, route_id):
    """Detalle de una ruta específica"""
    route = get_object_or_404(Route, id=route_id)
    
    context = {
        'route': route,
    }
    return render(request, 'admin/route_detail.html', context)


@login_required
@admin_required
def admin_route_edit(request, route_id):
    """Editar una ruta"""
    route = get_object_or_404(Route, id=route_id)
    
    if request.method == 'POST':
        # Actualizar datos de la ruta
        route.name = request.POST.get('name', route.name)
        route.description = request.POST.get('description', route.description)
        route.difficulty = request.POST.get('difficulty', route.difficulty)
        route.duration = request.POST.get('duration', route.duration)  # Cambiado de duration_days a duration
        route.price = request.POST.get('price', route.price)
        route.max_participants = request.POST.get('max_participants', route.max_participants)
        route.is_active = request.POST.get('is_active') == 'on'
        
        route.save()
        messages.success(request, f'Ruta {route.name} actualizada correctamente.')
        return redirect('trekly_admin_route_detail', route_id=route.id)
    
    context = {
        'route': route,
    }
    return render(request, 'admin/route_edit.html', context)


@login_required
@admin_required
def admin_route_toggle_active(request, route_id):
    """Activar/desactivar una ruta"""
    route = get_object_or_404(Route, id=route_id)
    route.is_active = not route.is_active
    route.save()
    
    status = 'activada' if route.is_active else 'desactivada'
    messages.success(request, f'Ruta {route.name} {status} correctamente.')
    return redirect('trekly_admin_routes')


@login_required
@admin_required
def admin_route_create(request):
    """Crear una nueva ruta"""
    if request.method == 'POST':
        try:
            # Crear nueva ruta
            route = Route()
            route.name = request.POST.get('name')
            route.description = request.POST.get('description')
            route.difficulty = request.POST.get('difficulty')
            route.duration = int(request.POST.get('duration', 1))  # Convertir a int y valor por defecto
            route.price = float(request.POST.get('price', 0))  # Convertir a float
            route.max_participants = int(request.POST.get('max_participants', 1))  # Convertir a int
            route.location = request.POST.get('location', '')
            route.created_by = request.user
            route.is_active = request.POST.get('is_active') == 'on'
            
            route.save()
            messages.success(request, f'Ruta {route.name} creada correctamente.')
            return redirect('trekly_admin_route_detail', route_id=route.id)
        except Exception as e:
            messages.error(request, f'Error al crear la ruta: {str(e)}')
            return redirect('trekly_admin_route_create')
    
    # Obtener lista de guías para asignar
    guides = User.objects.filter(is_guide=True)
    
    context = {
        'guides': guides,
    }
    return render(request, 'admin/route_create.html', context)
