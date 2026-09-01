from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from backend.models.user import User
from backend.utils.auth_middleware import token_required
from config import Config
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Faltan credenciales'}), 400
        
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not check_password_hash(user.hashed_password, data.get('password')):
        return jsonify({'error': 'Credenciales inválidas'}), 401
        
    token = jwt.encode({
        'sub': str(user.id),
        'email': user.email,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, Config.SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    })

@auth_bp.route('/me', methods=['GET'], strict_slashes=False)
@token_required
def me(current_user):
    return jsonify(current_user.to_dict())
