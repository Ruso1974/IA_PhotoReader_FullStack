"""
Rutas de Autenticación
Blueprint para manejo de registro y login
"""

from flask import Blueprint, request, jsonify
from user_manager import UserManager

# Crear Blueprint para autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Instancia del gestor de usuarios
user_manager = UserManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    POST /api/auth/register
    Body: {"username": "juan", "email": "juan@email.com", "password": "123456"}
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos: username, email, password'
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        
        # Validaciones básicas
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'message': 'Todos los campos son obligatorios'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': 'La contraseña debe tener al menos 6 caracteres'
            }), 400
        
        # Registrar usuario
        success = user_manager.register_user(username, email, password)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Usuario {username} registrado exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Error al registrar usuario. Posiblemente ya existe.'
            }), 409
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /api/auth/login
    Body: {"username": "juan", "password": "123456"}
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or not all(k in data for k in ('username', 'password')):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos: username, password'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username y password son obligatorios'
            }), 400
        
        # Autenticar usuario
        user = user_manager.login_user(username, password)
        
        if user:
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'user': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciales incorrectas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    POST /api/auth/logout
    Cerrar sesión (en el futuro se puede implementar con JWT)
    """
    return jsonify({
        'success': True,
        'message': 'Sesión cerrada exitosamente'
    }), 200
