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
    query = User.query

    search = request.args.get('search', '').strip()
    if search:
        search_term = f"%{search}%"
        query = query.filter(db.or_(
            User.email.ilike(search_term),
            User.full_name.ilike(search_term)
        ))

    role = request.args.get('role', '').strip()
    if role:
        query = query.filter(User.role == role)

    users = query.order_by(User.created_at.desc()).all()
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
        role=data.get('role'),
        empresa=data.get('empresa'),
        departamento=data.get('departamento')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<string:user_id>/password', methods=['PATCH'], strict_slashes=False)
@token_required
@admin_required
def update_user_password(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    data = request.get_json() or {}
    new_password = (data.get('password') or '').strip()
    if not new_password:
        return jsonify({'error': 'La nueva contraseña es requerida'}), 400

    try:
        user.hashed_password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Contraseña actualizada exitosamente', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<string:user_id>', methods=['DELETE'], strict_slashes=False)
@token_required
@admin_required
def delete_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if str(user.id) == str(current_user.id):
        return jsonify({'error': 'No puede eliminar su propio usuario activo'}), 400

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
