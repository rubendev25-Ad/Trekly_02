"""
User Controllers - View layer for User operations.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.services import UserService


user_service = UserService()


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validar que las contraseñas coincidan
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'users/register.html')
        
        # Validar longitud de contraseña
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'users/register.html')
        
        # Generar username único desde el email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while user_service.repository.exists_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1
        
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'is_guide': False,
        }

        user = user_service.create_user(user_data)

        if user:
            # Autenticar con el backend correcto
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido a Trekly.')
            return redirect('home')
        else:
            messages.error(request, 'Error al crear la cuenta. El email ya está registrado.')

    return render(request, 'users/register.html')


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Buscar usuario por email
        try:
            user_obj = user_service.repository.get_by_email(email)
            if user_obj:
                # Autenticar con username (Django lo requiere)
                user = authenticate(request, username=user_obj.username, password=password)
                
                if user is not None:
                    # Especificar el backend
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')
                    next_url = request.GET.get('next', 'home')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Contraseña incorrecta.')
            else:
                messages.error(request, 'No existe una cuenta con este email.')
        except Exception as e:
            messages.error(request, 'Error al iniciar sesión.')

    return render(request, 'users/login.html')


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('home')


@login_required
def profile_view(request, username=None):
    """User profile view."""
    if username:
        user = user_service.get_user_by_username(username)
    else:
        user = request.user

    if not user:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('home')

    context = {
        'profile_user': user,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile view."""
    if request.method == 'POST':
        # Actualizar directamente el usuario
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.bio = request.POST.get('bio', user.bio) if hasattr(user, 'bio') else ''
        user.location = request.POST.get('location', user.location) if hasattr(user, 'location') else ''

        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        try:
            user.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')
    
    return render(request, 'users/profile_edit.html')


def guides_list_view(request):
    """List all guides view."""
    guides = user_service.get_guides()
    context = {
        'guides': guides,
    }
    return render(request, 'users/guides_list.html', context)
