"""
User model for Trekly platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes additional fields for profile and guide status.
    """
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name='Imagen de perfil'
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        verbose_name='Biografía'
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ubicación'
    )
    is_guide = models.BooleanField(
        default=False,
        verbose_name='¿Es guía?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username
