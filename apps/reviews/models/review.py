"""
Review model for Trekly platform.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.routes.models import Route


class Review(models.Model):
    """
    Review model representing a user review for a route.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Usuario'
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Ruta'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calificación'
    )
    comment = models.TextField(
        verbose_name='Comentario'
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
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-created_at']
        unique_together = ['user', 'route']  # One review per user per route

    def __str__(self):
        return f"{self.user.username} - {self.route.title} - {self.rating}★"
