from flask import Blueprint, request, jsonify
from backend.models.ticket import db
from backend.models.categoria import Categoria
from backend.utils.auth_middleware import token_required, ticket_admin_required

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
@token_required
def get_categorias(current_user):
    query = Categoria.query

    # Si se especifica departamento_destino en la petición (ej. al crear un ticket de Data), aplicar ese filtro
    depto_filter = request.args.get('departamento_destino')
    if depto_filter:
        query = query.filter_by(departamento_destino=depto_filter)
    else:
        # De lo contrario, si es administrador de área sin filtro explícito, restringir a su departamento
        if current_user.role == 'Admin Data':
            query = query.filter_by(departamento_destino='BI')
        elif current_user.role == 'Admin HelpDesk':
            query = query.filter_by(departamento_destino='HELPDESK')

    categorias = query.order_by(Categoria.nombre.asc()).all()
    return jsonify([c.to_dict() for c in categorias]), 200


@categorias_bp.route('/', methods=['POST'])
@token_required
@ticket_admin_required
def create_categoria(current_user):
    data = request.get_json() or {}
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'error': 'El nombre de la categoría es requerido'}), 400

    # Determinación del departamento destino
    if current_user.role == 'Admin Data':
        departamento_destino = 'BI'
    elif current_user.role == 'Admin HelpDesk':
        departamento_destino = 'HELPDESK'
    else:
        departamento_destino = data.get('departamento_destino', '').strip()

    if departamento_destino not in ['BI', 'HELPDESK']:
        return jsonify({'error': 'Debe especificar un departamento destino válido (BI o HELPDESK)'}), 400

    # Validar duplicados en el mismo departamento
    existing = Categoria.query.filter_by(nombre=nombre, departamento_destino=departamento_destino).first()
    if existing:
        return jsonify({'error': f'Ya existe la categoría "{nombre}" en el área de {departamento_destino}'}), 400

    nueva_categoria = Categoria(
        nombre=nombre,
        departamento_destino=departamento_destino
    )

    db.session.add(nueva_categoria)
    db.session.commit()

    return jsonify(nueva_categoria.to_dict()), 201


@categorias_bp.route('/<id>', methods=['DELETE'])
@token_required
@ticket_admin_required
def delete_categoria(current_user, id):
    categoria = Categoria.query.filter_by(id=id).first()
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    # Restricción por área
    if current_user.role == 'Admin Data' and categoria.departamento_destino != 'BI':
        return jsonify({'error': 'No tiene permisos para eliminar categorías de otro departamento'}), 403
    if current_user.role == 'Admin HelpDesk' and categoria.departamento_destino != 'HELPDESK':
        return jsonify({'error': 'No tiene permisos para eliminar categorías de otro departamento'}), 403

    db.session.delete(categoria)
    db.session.commit()

    return jsonify({'message': 'Categoría eliminada exitosamente'}), 200
