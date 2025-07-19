<script setup>
import { ref } from 'vue'
import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'

const currentView = ref('login') // 'login', 'register', 'dashboard'
const user = ref(null)

const switchToRegister = () => {
  currentView.value = 'register'
}

const switchToLogin = () => {
  currentView.value = 'login'
}

const handleLoginSuccess = (userData) => {
  user.value = userData
  currentView.value = 'dashboard'
}

const handleRegisterSuccess = () => {
  currentView.value = 'login'
}

const logout = () => {
  user.value = null
  localStorage.removeItem('user')
  currentView.value = 'login'
}
</script>

<template>
  <div class="app">
    <header>
      <h1>🔐 Sistema de Gestión de Usuarios</h1>
      <p v-if="user" class="welcome">¡Bienvenido, {{ user.username }}!</p>
    </header>

    <main>
      <!-- Vista de Login -->
      <LoginForm 
        v-if="currentView === 'login'"
        @switch-to-register="switchToRegister"
        @login-success="handleLoginSuccess"
      />
      
      <!-- Vista de Registro -->
      <RegisterForm 
        v-if="currentView === 'register'"
        @switch-to-login="switchToLogin"
        @register-success="handleRegisterSuccess"
      />
      
      <!-- Dashboard después del login -->
      <div v-if="currentView === 'dashboard'" class="dashboard">
        <h2>Panel de Usuario</h2>
        <div class="user-info">
          <p><strong>ID:</strong> {{ user.id }}</p>
          <p><strong>Usuario:</strong> {{ user.username }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Fecha de registro:</strong> {{ new Date(user.created_at).toLocaleDateString() }}</p>
        </div>
        
        <button @click="logout" class="logout-btn">Cerrar Sesión</button>
      </div>
    </main>

    <footer>
      <p>🚀 Conectado con Flask API en http://localhost:8000</p>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Arial', sans-serif;
}

header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2rem;
  text-align: center;
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: bold;
}

.welcome {
  margin: 0;
  font-size: 1.2rem;
  opacity: 0.9;
}

main {
  flex: 1;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dashboard {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.dashboard h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.user-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.user-info p {
  margin: 0.5rem 0;
  color: #555;
}

.logout-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c82333;
}

footer {
  background: rgba(0, 0, 0, 0.2);
  padding: 1rem;
  text-align: center;
  color: white;
  font-size: 0.9rem;
}

footer p {
  margin: 0;
  opacity: 0.8;
}
</style>
