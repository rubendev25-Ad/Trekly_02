"""
URL configuration for users app.
"""
from django.urls import path
from allauth.socialaccount.providers.google.views import oauth2_login
from apps.users.controllers import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_edit_view,
    guides_list_view,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),  # Movido ANTES de profile_detail
    path('profile/<str:username>/', profile_view, name='profile_detail'),
    path('guides/', guides_list_view, name='guides_list'),
    
    # Google OAuth
    path('google/login/', oauth2_login, name='google_login'),
]
