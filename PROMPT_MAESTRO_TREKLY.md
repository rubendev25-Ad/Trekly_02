# 🧠 PROMPT MAESTRO — Proyecto Trekly

> 🚀 **Objetivo:** Crear desde cero una plataforma web llamada **Trekly**, desarrollada en **Django + Django REST Framework + PostgreSQL**, con una arquitectura limpia, modular y escalable.  
> El sistema permitirá gestionar rutas turísticas, usuarios, reservas y reseñas.

---

## 🏗️ 1. Estructura general del proyecto

Genera un proyecto Django con las siguientes características:

```
trekly/
│
├── manage.py
├── trekly/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/
│   ├── users/
│   ├── routes/
│   ├── bookings/
│   ├── reviews/
│   └── api/
│
├── templates/
├── static/
│
└── requirements.txt
```

---

## 🧱 2. Arquitectura — Clean Architecture (adaptada a Django)

Cada app tendrá esta estructura base:

```
app_name/
│
├── models/
├── repositories/
├── services/
├── controllers/
├── urls.py
└── tests/
```

Cada capa se comunica solo con la siguiente (controlador → servicio → repositorio → modelo).  
Evita lógica de negocio directamente en las vistas.

---

## ⚙️ 3. Configuración base

1. Configurar **PostgreSQL** como base de datos.  
2. Activar **Django REST Framework**.  
3. Crear un **superusuario**.  
4. Configurar archivos estáticos.  
5. Habilitar CORS si el frontend externo lo requiere.

---

## 👥 4. Apps y modelos principales

### `users`
- Campos: `username`, `email`, `password`, `first_name`, `last_name`, `profile_image`, `bio`, `location`, `is_guide`.

### `routes`
- Modelo: `Route`
  - `title`, `description`, `location`, `difficulty`, `duration`, `price`, `image`, `created_by`, `created_at`.

### `bookings`
- Modelo: `Booking`
  - `user`, `route`, `date`, `participants`, `status` (`pending`, `confirmed`, `cancelled`).

### `reviews`
- Modelo: `Review`
  - `user`, `route`, `rating`, `comment`, `created_at`.

---

## 🔌 5. API REST (app `api/`)

Configurar rutas como:

```
/api/users/
/api/routes/
/api/bookings/
/api/reviews/
```

Usar `ViewSets` y `Routers` automáticos con autenticación JWT.

---

## 🎨 6. Frontend integrado (HTML + CSS + Bootstrap)

- `index.html` → página principal.
- `route_detail.html` → detalle de ruta.
- `profile.html` → perfil del usuario.
- `booking_list.html` → reservas del usuario.
- Navbar con enlaces a Inicio, Explorar, Mis Reservas, Perfil.

---

## 🔐 7. Autenticación

- Login / Logout / Registro.
- Campo `is_guide` para distinguir guías y viajeros.
- Vistas restringidas con `@login_required`.

---

## 📦 8. Buenas prácticas

- Documentar con docstrings.
- Separar lógica de negocio en `services/`.
- Usar `serializers.py` limpios.
- Agregar `__str__()` a modelos.
- Configurar `.env`.
- Mantener estilo PEP8.

---

## 🧪 9. Pruebas

- Crear pruebas unitarias por app.
- Comando: `python manage.py test`.

---

## 📘 10. Extensiones futuras

- Notificaciones o chat.
- Mapas (Leaflet.js o Google Maps API).
- Pasarela de pago.
- App móvil futura usando la API.

---

## 🧩 11. `requirements.txt`

```
Django==5.1
djangorestframework==3.15
psycopg2-binary==2.9
python-dotenv==1.0
Pillow==10.0
django-cors-headers==4.3
```

---

## ✅ 12. Instrucciones finales para Copilot

> **Copilot**, genera el proyecto Django completo llamado `trekly` siguiendo esta estructura y especificaciones.  
> Usa buenas prácticas, nombres coherentes y mantén la arquitectura limpia.  
> Cada app debe contener modelos, servicios, repositorios, controladores, serializers, urls y tests.  
> Integra Bootstrap para el frontend, DRF para la API y PostgreSQL como base de datos.
