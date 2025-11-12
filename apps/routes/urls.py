"""
URL configuration for routes app.
"""
from django.urls import path
from django.views.generic import TemplateView
from apps.routes.controllers import (
    home_view,
    route_list_view,
    route_detail_view,
    route_create_view,
    route_edit_view,
    route_delete_view,
    my_routes_view,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='splash.html'), name='splash'),
    path('home/', home_view, name='home'),
    path('explore/', route_list_view, name='route_list'),
    path('route/<int:route_id>/', route_detail_view, name='route_detail'),
    path('route/create/', route_create_view, name='route_create'),
    path('route/<int:route_id>/edit/', route_edit_view, name='route_edit'),
    path('route/<int:route_id>/delete/', route_delete_view, name='route_delete'),
    path('my-routes/', my_routes_view, name='my_routes'),
]
