"""
Custom decorators for Trekly.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def trekly_admin_required(view_func):
    """Decorator to check if user is Trekly admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not (request.user.is_admin or request.user.is_superuser):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def guide_required(view_func):
    """Decorador que verifica si el usuario es un guía"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        if not request.user.is_guide:
            messages.error(request, 'No tienes permisos para acceder a esta página. Debes ser un guía.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator for views that checks that the user is 'trekly'.
    Redirects to home page if not authorized.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        
        # Solo permitir acceso al usuario 'trekly' o superusuarios
        if request.user.username != 'trekly' and not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para acceder a esta área.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
