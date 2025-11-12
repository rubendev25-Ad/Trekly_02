"""
Admin configuration for Routes app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from apps.routes.models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Admin configuration for Route model."""
    list_display = ['title', 'location', 'difficulty_badge', 'duration', 'price_display', 
                    'rating_display', 'bookings_count', 'guide_name', 'status_badge', 'created_at']
    list_filter = ['difficulty', 'is_active', 'created_at', 'location']
    search_fields = ['title', 'description', 'location', 'created_by__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'total_bookings', 'total_reviews']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    actions = ['activate_routes', 'deactivate_routes']

    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'description', 'image'),
            'classes': ('wide',)
        }),
        ('Detalles de la ruta', {
            'fields': ('location', 'difficulty', 'duration', 'price'),
            'classes': ('wide',)
        }),
        ('Gestión', {
            'fields': ('created_by', 'is_active'),
        }),
        ('Estadísticas', {
            'fields': ('average_rating', 'total_reviews', 'total_bookings', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def difficulty_badge(self, obj):
        """Display difficulty with color."""
        colors = {
            'easy': '#28a745',
            'moderate': '#ffc107',
            'hard': '#fd7e14',
            'expert': '#dc3545'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.difficulty, '#6c757d'),
            obj.get_difficulty_display()
        )
    difficulty_badge.short_description = 'Dificultad'
    
    def price_display(self, obj):
        """Display price formatted."""
        return format_html('<strong>${}</strong>', obj.price)
    price_display.short_description = 'Precio'
    
    def status_badge(self, obj):
        """Display active status."""
        if obj.is_active:
            return format_html(
                '<span style="color: white; background-color: #28a745; padding: 3px 8px; border-radius: 3px;">✓ Activa</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #dc3545; padding: 3px 8px; border-radius: 3px;">✗ Inactiva</span>'
        )
    status_badge.short_description = 'Estado'
    
    def guide_name(self, obj):
        """Display guide name."""
        return obj.created_by.get_full_name() or obj.created_by.username
    guide_name.short_description = 'Guía'
    
    def rating_display(self, obj):
        """Display average rating."""
        avg = obj.get_average_rating()
        if avg > 0:
            stars = '⭐' * int(avg)
            return format_html('{} <small>({})</small>', stars, f'{avg:.1f}')
        return '-'
    rating_display.short_description = 'Rating'
    
    def bookings_count(self, obj):
        """Display number of bookings."""
        count = obj.bookings.count()
        if count > 0:
            return format_html('<strong>{}</strong>', count)
        return '0'
    bookings_count.short_description = 'Reservas'
    
    def average_rating(self, obj):
        """Show average rating."""
        return f'{obj.get_average_rating():.1f} / 5.0'
    average_rating.short_description = 'Rating promedio'
    
    def total_reviews(self, obj):
        """Show total reviews."""
        return obj.get_reviews_count()
    total_reviews.short_description = 'Total de reseñas'
    
    def total_bookings(self, obj):
        """Show total bookings."""
        return obj.bookings.count()
    total_bookings.short_description = 'Total de reservas'
    
    def activate_routes(self, request, queryset):
        """Activate selected routes."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} ruta(s) activada(s).')
    activate_routes.short_description = '✓ Activar rutas seleccionadas'
    
    def deactivate_routes(self, request, queryset):
        """Deactivate selected routes."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} ruta(s) desactivada(s).')
    deactivate_routes.short_description = '✗ Desactivar rutas seleccionadas'
