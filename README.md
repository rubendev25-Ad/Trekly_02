# 🏔️ Trekly - Plataforma de Turismo de Aventura

Trekly es una aplicación web moderna para la gestión de rutas de trekking y turismo de aventura, construida con Django.

## ✨ Características

- 🗺️ **Gestión de Rutas**: Crear, editar y administrar rutas de trekking
- 👤 **Sistema de Usuarios**: Registro, login, perfiles personalizados
- 🎯 **Roles**: Usuarios regulares, guías y administradores
- 📊 **Dashboard Administrativo**: Panel personalizado para administradores
- 🎨 **Diseño Moderno**: Interfaz juvenil y motivadora
- 📱 **Responsive**: Diseño adaptable a todos los dispositivos
- 🔐 **Autenticación**: Sistema seguro de autenticación y autorización

## 🚀 Tecnologías

- **Backend**: Django 5.1
- **Base de datos**: SQLite (desarrollo)
- **Frontend**: Bootstrap 5, CSS personalizado
- **Autenticación**: Django Auth + Google OAuth

## 📋 Requisitos

- Python 3.11+
- pip
- virtualenv (recomendado)

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/rubendev25-Ad/Trekly_02.git
   cd Trekly_02
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

8. **Acceder a la aplicación**
   - Aplicación principal: `http://127.0.0.1:8000/`
   - Admin de Django: `http://127.0.0.1:8000/admin/`
   - Dashboard personalizado: `http://127.0.0.1:8000/trekly-admin/`

## 📁 Estructura del Proyecto

```
trekly/
├── apps/
│   ├── routes/          # App de rutas
│   ├── tours/           # App de tours
│   └── users/           # App de usuarios
├── static/              # Archivos estáticos
│   ├── css/
│   └── images/
├── templates/           # Templates HTML
├── trekly/              # Configuración del proyecto
└── manage.py
```

## 🎯 Funcionalidades Principales

### Para Usuarios
- Registro e inicio de sesión
- Explorar rutas disponibles
- Reservar tours
- Gestionar perfil personal

### Para Guías
- Crear y gestionar rutas
- Ver reservaciones
- Actualizar información de tours

### Para Administradores
- Dashboard personalizado en `/trekly-admin/`
- Gestión completa de usuarios
- Gestión de rutas (crear, editar, activar/desactivar)
- Asignación de roles y permisos
- Estadísticas del sistema

## 🔐 Usuarios de Prueba

- **Admin**: Usuario `trekly` (acceso al dashboard personalizado)

## 🎨 Diseño

El proyecto cuenta con un diseño moderno y juvenil con:
- Colores vibrantes y naturales
- Animaciones suaves
- Interfaz intuitiva
- Gradientes modernos
- Efectos hover dinámicos

## 📝 Licencia

Este proyecto es de código abierto.

## 👥 Autor

Desarrollado para la gestión de turismo de aventura.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del proyecto y envía un pull request.

---

⭐ Si te gusta este proyecto, no olvides darle una estrella!
