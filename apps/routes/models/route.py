"""
Route model for Trekly platform.
"""
from django.db import models
from django.conf import settings


class Route(models.Model):
    """
    Route model representing a tourist route/trek.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Fácil'),
        ('moderate', 'Moderada'),
        ('hard', 'Difícil'),
        ('expert', 'Experto'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name='Título'
    )
    description = models.TextField(
        verbose_name='Descripción'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='Ubicación'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='moderate',
        verbose_name='Dificultad'
    )
    duration = models.IntegerField(
        help_text='Duración en horas',
        verbose_name='Duración (horas)'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio'
    )
    image = models.ImageField(
        upload_to='routes/',
        blank=True,
        null=True,
        verbose_name='Imagen'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='routes',
        verbose_name='Creado por'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )

    class Meta:
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_average_rating(self):
        """Calculate average rating from reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(r.rating for r in reviews) / reviews.count()
        return 0

    def get_reviews_count(self):
        """Get total number of reviews."""
        return self.reviews.count()
