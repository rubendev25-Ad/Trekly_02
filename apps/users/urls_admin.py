"""
URL configuration for custom Trekly admin.
"""
from django.urls import path
from apps.users.controllers.admin_controller import (
    admin_dashboard,
    admin_users_list,
    admin_user_detail,
    admin_user_edit,
    admin_stats,
    admin_routes_list,
    admin_route_detail,
    admin_route_edit,
    admin_route_toggle_active,
    admin_route_create,
)

urlpatterns = [
    path('', admin_dashboard, name='trekly_admin_dashboard'),
    path('users/', admin_users_list, name='trekly_admin_users'),
    path('users/<int:user_id>/', admin_user_detail, name='trekly_admin_user_detail'),
    path('users/<int:user_id>/edit/', admin_user_edit, name='trekly_admin_user_edit'),
    path('stats/', admin_stats, name='trekly_admin_stats'),
    path('routes/', admin_routes_list, name='trekly_admin_routes'),
    path('routes/<int:route_id>/', admin_route_detail, name='trekly_admin_route_detail'),
    path('routes/<int:route_id>/edit/', admin_route_edit, name='trekly_admin_route_edit'),
    path('routes/<int:route_id>/toggle/', admin_route_toggle_active, name='trekly_admin_route_toggle'),
    path('routes/create/', admin_route_create, name='trekly_admin_route_create'),
]
