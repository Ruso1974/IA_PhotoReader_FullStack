<template>
  <div class="login-container">
    <h2>Iniciar Sesión</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">Usuario:</label>
        <input
          id="username"
          v-model="loginData.username"
          type="text"
          placeholder="Ingresa tu usuario"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input
          id="password"
          v-model="loginData.password"
          type="password"
          placeholder="Ingresa tu contraseña"
          required
        />
      </div>
      
      <button type="submit" :disabled="loading" class="login-btn">
        {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
      </button>
    </form>
    
    <!-- Mostrar mensajes -->
    <div v-if="message" :class="messageClass" class="message">
      {{ message }}
    </div>
    
    <p class="switch-form">
      ¿No tienes cuenta? 
      <a href="#" @click="$emit('switch-to-register')">Regístrate aquí</a>
    </p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginForm',
  data() {
    return {
      loginData: {
        username: '',
        password: ''
      },
      loading: false,
      message: '',
      messageClass: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.message = ''
      
      try {
        const response = await axios.post('http://localhost:8000/api/auth/login', {
          username: this.loginData.username,
          password: this.loginData.password
        })
        
        if (response.data.success) {
          this.message = response.data.message
          this.messageClass = 'success'
          
          // Guardar datos del usuario si es necesario
          localStorage.setItem('user', JSON.stringify(response.data.user))
          
          // Emitir evento de login exitoso
          this.$emit('login-success', response.data.user)
          
        } else {
          this.message = response.data.message
          this.messageClass = 'error'
        }
        
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.message
        } else {
          this.message = 'Error de conexión con el servidor'
        }
        this.messageClass = 'error'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.login-btn {
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.login-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.switch-form {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.switch-form a {
  color: #007bff;
  text-decoration: none;
}

.switch-form a:hover {
  text-decoration: underline;
}
</style>
