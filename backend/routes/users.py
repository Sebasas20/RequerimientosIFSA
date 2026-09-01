from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.utils.auth_middleware import token_required, admin_required
from werkzeug.security import generate_password_hash
from backend.models.ticket import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'], strict_slashes=False)
@token_required
@admin_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@users_bp.route('/', methods=['POST'], strict_slashes=False)
@token_required
@admin_required
def create_user(current_user):
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('full_name') or not data.get('role'):
        return jsonify({'error': 'Todos los campos son requeridos (full_name, email, password, role)'}), 400
        
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return jsonify({'error': 'El correo electrónico ya está registrado'}), 400
        
    hashed_pwd = generate_password_hash(data.get('password'))
    
    new_user = User(
        full_name=data.get('full_name'),
        email=data.get('email'),
        hashed_password=hashed_pwd,
        role=data.get('role')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
