"""
Admin configuration for Reviews app.
"""
from django.contrib import admin
from django.utils.html import format_html
from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for Review model."""
    list_display = ['user_name', 'route_title', 'rating_stars', 'comment_preview', 'created_at']
    list_filter = ['rating', 'created_at', 'route__difficulty']
    search_fields = ['user__username', 'route__title', 'comment', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información de la reseña', {
            'fields': ('user', 'route', 'rating', 'comment'),
            'classes': ('wide',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_name(self, obj):
        """Display user full name."""
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'Usuario'
    
    def route_title(self, obj):
        """Display route title."""
        return obj.route.title
    route_title.short_description = 'Ruta'
    
    def rating_stars(self, obj):
        """Display rating as stars."""
        stars = '⭐' * obj.rating
        empty_stars = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107;">{}</span><span style="color: #ddd;">{}</span> <small>({})</small>',
            stars, empty_stars, obj.rating
        )
    rating_stars.short_description = 'Calificación'
    
    def comment_preview(self, obj):
        """Display truncated comment."""
        if len(obj.comment) > 50:
            return f'{obj.comment[:50]}...'
        return obj.comment
    comment_preview.short_description = 'Comentario'
