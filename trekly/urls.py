"""
URL configuration for trekly project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import admin customization
from . import admin as custom_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trekly-admin/', include('apps.users.urls_admin')),  # Custom Trekly Admin
    path('api/', include('apps.api.urls')),
    path('accounts/', include('allauth.urls')),  # Django-allauth URLs
    path('users/', include('apps.users.urls')),
    path('routes/', include('apps.routes.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('', include('apps.routes.urls')),  # Homepage
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
