"""
Admin configuration for Bookings app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin configuration for Booking model."""
    list_display = ['booking_id', 'user_name', 'route_title', 'date', 'participants', 
                    'status_badge', 'total_price_display', 'created_at']
    list_filter = ['status', 'date', 'created_at', 'route__difficulty']
    search_fields = ['user__username', 'route__title', 'user__email', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'total_price', 'calculated_price']
    list_per_page = 25
    date_hierarchy = 'date'
    
    actions = ['confirm_bookings', 'complete_bookings', 'cancel_bookings']

    fieldsets = (
        ('Información de la reserva', {
            'fields': ('user', 'route', 'date', 'participants'),
            'classes': ('wide',)
        }),
        ('Estado y precio', {
            'fields': ('status', 'total_price', 'calculated_price'),
        }),
        ('Notas adicionales', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Fechas del sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_id(self, obj):
        """Display booking ID."""
        return format_html('<strong>#{}</strong>', obj.id)
    booking_id.short_description = 'ID'
    
    def user_name(self, obj):
        """Display user full name."""
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'Usuario'
    
    def route_title(self, obj):
        """Display route title."""
        return obj.route.title
    route_title.short_description = 'Ruta'
    
    def status_badge(self, obj):
        """Display status with color."""
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'cancelled': '#dc3545',
            'completed': '#17a2b8'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def total_price_display(self, obj):
        """Display total price formatted."""
        return format_html('<strong style="color: #28a745;">${}</strong>', obj.total_price)
    total_price_display.short_description = 'Total'
    
    def calculated_price(self, obj):
        """Show calculated price breakdown."""
        return f'${obj.route.price} × {obj.participants} = ${obj.total_price}'
    calculated_price.short_description = 'Cálculo del precio'
    
    def confirm_bookings(self, request, queryset):
        """Confirm selected bookings."""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} reserva(s) confirmada(s).')
    confirm_bookings.short_description = '✓ Confirmar reservas'
    
    def complete_bookings(self, request, queryset):
        """Mark bookings as completed."""
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'{updated} reserva(s) completada(s).')
    complete_bookings.short_description = '✓ Marcar como completadas'
    
    def cancel_bookings(self, request, queryset):
        """Cancel selected bookings."""
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'{updated} reserva(s) cancelada(s).')
    cancel_bookings.short_description = '✗ Cancelar reservas'
    
    def changelist_view(self, request, extra_context=None):
        """Add statistics to the changelist view."""
        extra_context = extra_context or {}
        
        # Calculate statistics
        stats = Booking.objects.aggregate(
            total_bookings=Count('id'),
            total_revenue=Sum('total_price'),
            pending=Count('id', filter=admin.models.Q(status='pending')),
            confirmed=Count('id', filter=admin.models.Q(status='confirmed')),
            completed=Count('id', filter=admin.models.Q(status='completed')),
            cancelled=Count('id', filter=admin.models.Q(status='cancelled')),
        )
        
        extra_context['stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)
