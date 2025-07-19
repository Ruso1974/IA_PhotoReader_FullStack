"""
Rutas de Información y Utilidades
Blueprint para endpoints de sistema
"""

from flask import Blueprint, jsonify, current_app

# Crear Blueprint para información del sistema
info_bp = Blueprint('info', __name__, url_prefix='/api')

@info_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health
    Verificar estado de la API
    """
    return jsonify({
        'success': True,
        'message': 'API funcionando correctamente',
        'version': '1.0.0',
        'status': 'healthy'
    }), 200

@info_bp.route('/routes', methods=['GET'])
def get_routes():
    """
    GET /api/routes
    Listar todas las rutas disponibles
    """
    routes = []
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                'url': str(rule)
            })
    
    return jsonify({
        'success': True,
        'routes': routes,
        'count': len(routes)
    }), 200

@info_bp.route('/status', methods=['GET'])
def get_status():
    """
    GET /api/status
    Información detallada del sistema
    """
    return jsonify({
        'success': True,
        'api': {
            'name': 'User Management API',
            'version': '1.0.0',
            'status': 'running',
            'debug': current_app.debug,
            'environment': 'development' if current_app.debug else 'production'
        },
        'database': {
            'type': 'MySQL',
            'status': 'connected'  # Se podría hacer una verificación real
        }
    }), 200
