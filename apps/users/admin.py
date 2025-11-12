"""
Admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""
    list_display = ['username', 'email', 'full_name', 'role_badges', 'location', 'created_at']
    list_filter = ['is_guide', 'is_staff', 'is_superuser', 'is_active', 'created_at']  # Removí temporalmente 'is_admin'
    search_fields = ['username', 'email', 'first_name', 'last_name', 'location']
    ordering = ['-created_at']
    list_per_page = 25
    
    actions = ['make_guide', 'remove_guide', 'make_admin', 'remove_admin', 'activate_users', 'deactivate_users']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('profile_image', 'bio', 'location', 'phone_number'),
            'classes': ('wide',)
        }),
        ('Roles y Permisos', {
            'fields': ('is_guide',),  # Removí temporalmente 'is_admin'
            'classes': ('wide',),
            'description': 'Gestiona los roles del usuario en Trekly'
        }),
        ('Fechas importantes', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('email', 'first_name', 'last_name'),
            'classes': ('wide',)
        }),
        ('Roles', {
            'fields': ('is_guide',),  # Removí temporalmente 'is_admin'
            'classes': ('wide',)
        }),
    )
    
    def full_name(self, obj):
        return obj.get_full_name() or '-'
    full_name.short_description = 'Nombre completo'
    
    def role_badges(self, obj):
        badges = []
        if obj.is_superuser:
            badges.append('<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px; margin-right: 5px;">👑 Super Admin</span>')
        elif getattr(obj, 'is_admin', False):
            badges.append('<span style="color: white; background-color: #007bff; padding: 3px 10px; border-radius: 3px; margin-right: 5px;">🛡️ Admin</span>')
        if obj.is_guide:
            badges.append('<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px; margin-right: 5px;">✓ Guía</span>')
        if not badges:
            badges.append('<span style="color: #666;">👤 Usuario</span>')
        return format_html(''.join(badges))
    role_badges.short_description = 'Roles'
    
    def make_guide(self, request, queryset):
        updated = queryset.update(is_guide=True)
        self.message_user(request, f'{updated} usuario(s) promovido(s) a Guía.')
    make_guide.short_description = '✓ Promover a Guía'
    
    def remove_guide(self, request, queryset):
        updated = queryset.update(is_guide=False)
        self.message_user(request, f'{updated} usuario(s) removido(s) como Guía.')
    remove_guide.short_description = '✗ Remover como Guía'
    
    def make_admin(self, request, queryset):
        updated = queryset.update(is_admin=True)
        self.message_user(request, f'{updated} usuario(s) promovido(s) a Administrador.')
    make_admin.short_description = '🛡️ Promover a Admin'
    
    def remove_admin(self, request, queryset):
        updated = queryset.update(is_admin=False)
        self.message_user(request, f'{updated} usuario(s) removido(s) como Admin.')
    remove_admin.short_description = '✗ Remover como Admin'
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} usuario(s) activado(s).')
    activate_users.short_description = '✓ Activar usuarios'
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} usuario(s) desactivado(s).')
    deactivate_users.short_description = '✗ Desactivar usuarios'
