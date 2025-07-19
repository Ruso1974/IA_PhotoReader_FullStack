#!/usr/bin/env python3
"""
API REST para Gestión de Usuarios con MySQL
Aplicación principal con estructura modular usando Blueprints
Autor: Pablo
Fecha: Julio 2025
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

# Importar Blueprints (routers)
from routes.auth import auth_bp
from routes.users import users_bp
from routes.info import info_bp

# Cargar variables de entorno
load_dotenv()

def create_app():
    """Factory function para crear la aplicación Flask"""
    
    # Crear aplicación Flask
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = True
    
    # Desactivar logs automáticos de Werkzeug para personalizar la salida
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Habilitar CORS para permitir requests desde frontend
    CORS(app)
    
    # Registrar Blueprints (routers)
    app.register_blueprint(auth_bp)      # /api/auth/*
    app.register_blueprint(users_bp)     # /api/users/*  
    app.register_blueprint(info_bp)      # /api/health, /api/routes, etc.
    
    # Ruta raíz
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'User Management API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'info': '/api/health'
            }
        }), 200
    
    # ==================== MANEJO DE ERRORES ====================
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint no encontrado',
            'error': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'Método HTTP no permitido',
            'error': 'Method Not Allowed'
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor',
            'error': 'Internal Server Error'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Solicitud inválida',
            'error': 'Bad Request'
        }), 400
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Configuración para desarrollo
    print("🚀 Iniciando API de Gestión de Usuarios...")
    print("📍 API disponible en: http://localhost:8000")
    print("📚 Documentación: Ver API_DOCS.md")
    print("⚠️  Presiona CTRL+C para detener el servidor")
    print("-" * 50)
    
    try:
        app.run(
            debug=True,           # Modo debug para desarrollo
            host='127.0.0.1',    # Solo localhost
            port=8000,           # Puerto 8000
            use_reloader=False   # Evitar doble inicio
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
