<template>
  <div class="register-container">
    <h2>Registrarse</h2>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="username">Usuario:</label>
        <input
          id="username"
          v-model="registerData.username"
          type="text"
          placeholder="Elige un nombre de usuario"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          id="email"
          v-model="registerData.email"
          type="email"
          placeholder="Ingresa tu email"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="password">Contraseña:</label>
        <input
          id="password"
          v-model="registerData.password"
          type="password"
          placeholder="Mínimo 6 caracteres"
          required
          minlength="6"
        />
      </div>
      
      <button type="submit" :disabled="loading" class="register-btn">
        {{ loading ? 'Registrando...' : 'Registrarse' }}
      </button>
    </form>
    
    <!-- Mostrar mensajes -->
    <div v-if="message" :class="messageClass" class="message">
      {{ message }}
    </div>
    
    <p class="switch-form">
      ¿Ya tienes cuenta? 
      <a href="#" @click="$emit('switch-to-login')">Inicia sesión aquí</a>
    </p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegisterForm',
  data() {
    return {
      registerData: {
        username: '',
        email: '',
        password: ''
      },
      loading: false,
      message: '',
      messageClass: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.message = ''
      
      try {
        const response = await axios.post('http://localhost:8000/api/auth/register', {
          username: this.registerData.username,
          email: this.registerData.email,
          password: this.registerData.password
        })
        
        if (response.data.success) {
          this.message = response.data.message + ' - Ahora puedes iniciar sesión'
          this.messageClass = 'success'
          
          // Limpiar formulario después de registro exitoso
          setTimeout(() => {
            this.registerData = { username: '', email: '', password: '' }
            this.$emit('register-success')
          }, 2000)
          
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
.register-container {
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

.register-form {
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
  border-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.25);
}

.register-btn {
  padding: 0.75rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-btn:hover:not(:disabled) {
  background-color: #218838;
}

.register-btn:disabled {
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
  color: #28a745;
  text-decoration: none;
}

.switch-form a:hover {
  text-decoration: underline;
}
</style>
