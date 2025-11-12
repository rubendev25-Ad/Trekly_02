# 🔐 Configurar Google OAuth para Trekly

## Pasos para obtener credenciales de Google:

### 1. Ir a Google Cloud Console
https://console.cloud.google.com/

### 2. Crear un nuevo proyecto
- Nombre: "Trekly"
- Hacer clic en "Crear"

### 3. Habilitar Google+ API
- Ir a "APIs y servicios" > "Biblioteca"
- Buscar "Google+ API"
- Hacer clic en "Habilitar"

### 4. Crear credenciales OAuth
- Ir a "APIs y servicios" > "Credenciales"
- Hacer clic en "Crear credenciales" > "ID de cliente de OAuth"
- Tipo de aplicación: "Aplicación web"
- Nombre: "Trekly Web App"

### 5. Configurar URIs autorizados
**Orígenes de JavaScript autorizados:**
```
http://localhost:8000
http://127.0.0.1:8000
```

**URIs de redireccionamiento autorizados:**
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
```

### 6. Copiar credenciales
- Copiar "Client ID" y "Client Secret"
- Pegarlos en el archivo `.env`:
```
GOOGLE_CLIENT_ID=tu-client-id-aqui.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret-aqui
```

### 7. Configurar en Django Admin
Después de ejecutar migraciones y crear superusuario:

1. Ir a: http://127.0.0.1:8000/admin
2. Navegar a: "Sites" > Editar "example.com"
3. Cambiar:
   - Domain name: `localhost:8000`
   - Display name: `Trekly`
4. Guardar

5. Ir a: "Social applications" > "Add social application"
6. Configurar:
   - Provider: `Google`
   - Name: `Google OAuth`
   - Client id: `[Tu Client ID]`
   - Secret key: `[Tu Client Secret]`
   - Sites: Seleccionar `localhost:8000` (mover a "Chosen sites")
7. Guardar

## 🚀 Listo para usar!

Ahora los usuarios podrán:
- Registrarse con email y contraseña
- Iniciar sesión con email y contraseña
- Iniciar sesión con Google
