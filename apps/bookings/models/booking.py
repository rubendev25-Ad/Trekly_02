"""
Booking model for Trekly platform.
"""
from django.db import models
from django.conf import settings
from apps.routes.models import Route


class Booking(models.Model):
    """
    Booking model representing a reservation for a route.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Usuario'
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Ruta'
    )
    date = models.DateField(
        verbose_name='Fecha'
    )
    participants = models.IntegerField(
        default=1,
        verbose_name='Participantes'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio total'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notas adicionales'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.route.title} - {self.date}"

    def calculate_total_price(self):
        """Calculate total price based on route price and participants."""
        return self.route.price * self.participants

    def save(self, *args, **kwargs):
        """Override save to calculate total price."""
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
