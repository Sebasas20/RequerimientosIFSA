import jwt
from functools import wraps
from flask import request, jsonify
from config import Config
from backend.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Format: "Bearer <token>"
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]
            
        if not token:
            return jsonify({'error': 'Token de autenticación faltante'}), 401
            
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = data.get('sub') or data.get('user_id')
            if not user_id:
                return jsonify({'error': 'Token inválido'}), 401
            current_user = User.query.filter_by(id=str(user_id)).first()
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Sesión expirada'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401
            
        return f(current_user, *args, **kwargs)
        
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'Administrador':
            return jsonify({'error': 'Acceso denegado: Se requieren permisos de Administrador'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def ticket_admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user.role not in ['Administrador', 'Admin Data', 'Admin HelpDesk']:
            return jsonify({'error': 'Acceso denegado: Se requieren permisos de administración de tickets'}), 403
        return f(current_user, *args, **kwargs)
    return decorated
