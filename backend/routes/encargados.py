from flask import Blueprint, request, jsonify
from backend.models.ticket import db
from backend.models.encargado import Encargado
from backend.utils.auth_middleware import token_required, ticket_admin_required

encargados_bp = Blueprint('encargados', __name__)

@encargados_bp.route('/', methods=['GET'])
@token_required
def get_encargados(current_user):
    query = Encargado.query

    # Filtrar automáticamente según el rol del usuario si es administrador de área
    if current_user.role == 'Admin Data':
        query = query.filter_by(departamento_destino='BI')
    elif current_user.role == 'Admin HelpDesk':
        query = query.filter_by(departamento_destino='HELPDESK')
    else:
        # Para Super Admin o usuarios generales, permitir filtro opcional por query param
        depto_filter = request.args.get('departamento_destino')
        if depto_filter:
            query = query.filter_by(departamento_destino=depto_filter)

    encargados = query.order_by(Encargado.nombre.asc()).all()
    return jsonify([e.to_dict() for e in encargados]), 200


@encargados_bp.route('/', methods=['POST'])
@token_required
@ticket_admin_required
def create_encargado(current_user):
    data = request.get_json() or {}
    nombre = data.get('nombre', '').strip()
    
    if not nombre:
        return jsonify({'error': 'El nombre del encargado es requerido'}), 400

    # Determinación automática del departamento
    if current_user.role == 'Admin Data':
        departamento_destino = 'BI'
    elif current_user.role == 'Admin HelpDesk':
        departamento_destino = 'HELPDESK'
    else:
        # Super Admin especifica el departamento destino
        departamento_destino = data.get('departamento_destino', '').strip()

    if departamento_destino not in ['BI', 'HELPDESK']:
        return jsonify({'error': 'Debe especificar un departamento destino válido (BI o HELPDESK)'}), 400

    # Validar duplicados en el mismo departamento
    existing = Encargado.query.filter_by(nombre=nombre, departamento_destino=departamento_destino).first()
    if existing:
        return jsonify({'error': f'Ya existe el encargado "{nombre}" registrado en el área de {departamento_destino}'}), 400

    nuevo_encargado = Encargado(
        nombre=nombre,
        departamento_destino=departamento_destino
    )

    db.session.add(nuevo_encargado)
    db.session.commit()

    return jsonify(nuevo_encargado.to_dict()), 201


@encargados_bp.route('/<id>', methods=['DELETE'])
@token_required
@ticket_admin_required
def delete_encargado(current_user, id):
    encargado = Encargado.query.filter_by(id=id).first()
    if not encargado:
        return jsonify({'error': 'Encargado no encontrado'}), 404

    # Restricción de borrado por departamento
    if current_user.role == 'Admin Data' and encargado.departamento_destino != 'BI':
        return jsonify({'error': 'No tiene permisos para eliminar encargados de otro departamento'}), 403
    if current_user.role == 'Admin HelpDesk' and encargado.departamento_destino != 'HELPDESK':
        return jsonify({'error': 'No tiene permisos para eliminar encargados de otro departamento'}), 403

    db.session.delete(encargado)
    db.session.commit()

    return jsonify({'message': 'Encargado eliminado exitosamente'}), 200
