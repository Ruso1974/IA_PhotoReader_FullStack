# 🌐 API REST - Gestión de Usuarios

## 🚀 Ejecutar la API

```bash
cd "/Users/pablobocchio/Proyectos Python/IA_PhotoReader"
"/Users/pablobocchio/Proyectos Python/IA_PhotoReader/.venv/bin/python" app.py
```

La API estará disponible en: **http://localhost:8000**

---

## 📋 Endpoints Disponibles (Con Routers/Blueprints)

### 🔐 **Autenticación** (`/api/auth`)

#### Registrar Usuario
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "juan123",
  "email": "juan@email.com", 
  "password": "micontraseña123"
}
```

#### Iniciar Sesión
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "juan123",
  "password": "micontraseña123"
}
```

#### Cerrar Sesión
```http
POST /api/auth/logout
```

### 👥 **Gestión de Usuarios** (`/api/users`)

#### Obtener Todos los Usuarios
```http
GET /api/users/
```

#### Obtener Usuario Específico
```http
GET /api/users/juan123
```

#### Eliminar Usuario
```http
DELETE /api/users/juan123
```

#### Cambiar Contraseña
```http
PUT /api/users/juan123/password
Content-Type: application/json

{
  "old_password": "micontraseña123",
  "new_password": "nuevacontraseña456"
}
```

### ℹ️ **Información del Sistema** (`/api`)

#### Estado de la API
```http
GET /api/health
```

#### Estado Detallado
```http
GET /api/status
```

#### Listar Rutas
```http
GET /api/routes
```

---

## 🌐 Ejemplos para Frontend

### **JavaScript/Fetch API**

```javascript
// Registrar usuario
async function registrarUsuario(username, email, password) {
  const response = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      email: email,
      password: password
    })
  });
  
  const data = await response.json();
  return data;
}

// Login
async function login(username, password) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });
  
  const data = await response.json();
  return data;
}

// Obtener usuarios
async function obtenerUsuarios() {
  const response = await fetch('http://localhost:8000/api/users/');
  const data = await response.json();
  return data;
}
```

### **React Example**

```jsx
import React, { useState } from 'react';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      const data = await response.json();
      
      if (data.success) {
        console.log('Login exitoso:', data.user);
        // Guardar usuario en estado, localStorage, etc.
      } else {
        console.error('Error:', data.message);
      }
    } catch (error) {
      console.error('Error de conexión:', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### **cURL Examples**

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@email.com", "password": "123456"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "123456"}'

# Obtener usuarios
curl http://localhost:8000/api/users/

# Eliminar usuario
curl -X DELETE http://localhost:8000/api/users/test

# Cambiar contraseña
curl -X PUT http://localhost:8000/api/users/test/password \
  -H "Content-Type: application/json" \
  -d '{"old_password": "123456", "new_password": "654321"}'
```

---

## 🔒 Códigos de Estado HTTP

- **200** - OK (éxito)
- **201** - Created (usuario registrado)
- **400** - Bad Request (datos inválidos)
- **401** - Unauthorized (credenciales incorrectas)
- **404** - Not Found (usuario no encontrado)
- **409** - Conflict (usuario ya existe)
- **500** - Internal Server Error (error del servidor)

---

## 🛠️ Tecnologías

- **Flask** - Framework web
- **Flask-CORS** - Manejo de CORS para frontend
- **bcrypt** - Hash de contraseñas
- **MySQL** - Base de datos
- **JSON** - Formato de intercambio de datos
