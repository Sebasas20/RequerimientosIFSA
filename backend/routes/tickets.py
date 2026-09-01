from flask import Blueprint, request, jsonify
from backend.models.ticket import db, Ticket
from backend.utils.validators import validate_json, sanitize_input
from backend.utils.auth_middleware import token_required, admin_required

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', strict_slashes=False, methods=['GET'])
@token_required
def get_tickets(current_user):
    try:
        query = Ticket.query
        
        # Filtrado por Rol
        if current_user.role == 'Usuario':
            query = query.filter(Ticket.creator_email == current_user.email)
        
        # Filtros Adicionales
        estado = request.args.get('estado')
        if estado:
            query = query.filter(Ticket.estado == estado)
            
        departamento = request.args.get('departamento')
        if departamento:
            query = query.filter(Ticket.departamento == departamento)
            
        tipo_solicitud = request.args.get('tipo_solicitud')
        if tipo_solicitud:
            query = query.filter(Ticket.tipo_solicitud == tipo_solicitud)
            
        search = request.args.get('search')
        if search:
            search_term = f"%{search}%"
            query = query.filter(db.or_(
                Ticket.nombre_solicitante.ilike(search_term),
                Ticket.id.ilike(search_term)
            ))

        tickets = query.order_by(Ticket.created_at.desc()).all()
        return jsonify([t.to_dict() for t in tickets]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tickets_bp.route('/', strict_slashes=False, methods=['POST'])
@token_required
@validate_json
def create_ticket(current_user):
    try:
        data = sanitize_input(request.get_json())
        
        required_fields = ['nombre_solicitante', 'empresa', 'departamento', 'descripcion', 'tipo_solicitud']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"El campo {field} es requerido"}), 400
                
        valid_tipos = ['Creación de Dashboards', 'Análisis profundo', 'Modelos Estadísticos/ML', 'Troubleshooting', 'Otros requerimientos']
        if data['tipo_solicitud'] not in valid_tipos:
            return jsonify({"error": "Tipo de solicitud inválido"}), 400

        new_ticket = Ticket(
            nombre_solicitante=data['nombre_solicitante'],
            empresa=data['empresa'],
            departamento=data['departamento'],
            descripcion=data['descripcion'],
            tipo_solicitud=data['tipo_solicitud'],
            creator_email=current_user.email
        )
        
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify(new_ticket.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@tickets_bp.route('/<string:ticket_id>', methods=['PATCH'])
@token_required
@admin_required
@validate_json
def update_ticket(current_user, ticket_id):
    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket no encontrado"}), 404
            
        data = sanitize_input(request.get_json())
        
        if 'estado' in data:
            nuevo_estado = data['estado']
            valid_estados = ['Creado / Esperando Asignación', 'Asignado/Desarrollo', 'Información Requerida', 'Pausado', 'Rechazado/Fuera de Alcance']
            if nuevo_estado not in valid_estados:
                return jsonify({"error": "Estado inválido"}), 400
                
            if nuevo_estado in ['Rechazado/Fuera de Alcance', 'Pausado', 'Información Requerida']:
                if not data.get('motivo_justificacion') and not ticket.motivo_justificacion:
                    return jsonify({"error": "Se requiere motivo de justificación para este estado"}), 400
            
            ticket.estado = nuevo_estado
            
        if 'prioridad' in data:
            valid_priorities = ['Prioridad 1', 'Prioridad 2', 'Prioridad 3', 'Prioridad 4']
            if data['prioridad'] not in valid_priorities and data['prioridad'] is not None:
                return jsonify({"error": "Prioridad inválida"}), 400
            ticket.prioridad = data['prioridad']
            
        if 'encargado' in data:
            ticket.encargado = data['encargado']
            if ticket.estado == 'Creado / Esperando Asignación':
                ticket.estado = 'Asignado/Desarrollo'
                
        if 'motivo_justificacion' in data:
            ticket.motivo_justificacion = data['motivo_justificacion']

        db.session.commit()
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
