"""
Rutas de Gestión de Usuarios
Blueprint para CRUD de usuarios
"""

from flask import Blueprint, request, jsonify
from user_manager import UserManager

# Crear Blueprint para usuarios
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Instancia del gestor de usuarios
user_manager = UserManager()

@users_bp.route('/', methods=['GET'])
def get_users():
    """
    GET /api/users/
    Obtener todos los usuarios
    """
    try:
        users = user_manager.get_all_users()
        
        return jsonify({
            'success': True,
            'users': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@users_bp.route('/<username>', methods=['GET'])
def get_user(username):
    """
    GET /api/users/juan
    Obtener información de un usuario específico
    """
    try:
        if not username or not username.strip():
            return jsonify({
                'success': False,
                'message': 'Username es requerido'
            }), 400
        
        # Buscar usuario (sin mostrar password)
        users = user_manager.get_all_users()
        user = next((u for u in users if u['username'] == username.strip()), None)
        
        if user:
            return jsonify({
                'success': True,
                'user': user
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Usuario {username} no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@users_bp.route('/<username>', methods=['DELETE'])
def delete_user(username):
    """
    DELETE /api/users/juan
    Eliminar un usuario específico
    """
    try:
        if not username or not username.strip():
            return jsonify({
                'success': False,
                'message': 'Username es requerido'
            }), 400
        
        success = user_manager.delete_user(username.strip())
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Usuario {username} eliminado exitosamente'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'No se pudo eliminar el usuario {username}'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@users_bp.route('/<username>/password', methods=['PUT'])
def change_password(username):
    """
    PUT /api/users/juan/password
    Body: {"old_password": "123456", "new_password": "654321"}
    """
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or not all(k in data for k in ('old_password', 'new_password')):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos: old_password, new_password'
            }), 400
        
        old_password = data['old_password']
        new_password = data['new_password']
        
        if not old_password or not new_password:
            return jsonify({
                'success': False,
                'message': 'Las contraseñas son obligatorias'
            }), 400
        
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'message': 'La nueva contraseña debe tener al menos 6 caracteres'
            }), 400
        
        # Cambiar contraseña
        success = user_manager.change_password(username, old_password, new_password)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Contraseña cambiada exitosamente para {username}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Error al cambiar contraseña. Verifique la contraseña actual.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error interno: {str(e)}'
        }), 500

@users_bp.route('/<username>/profile', methods=['PUT'])
def update_profile(username):
    """
    PUT /api/users/juan/profile
    Body: {"email": "nuevo@email.com"}
    Actualizar perfil de usuario (futuro feature)
    """
    return jsonify({
        'success': False,
        'message': 'Funcionalidad no implementada aún'
    }), 501
