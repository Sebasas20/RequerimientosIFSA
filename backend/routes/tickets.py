from flask import Blueprint, request, jsonify
from backend.models.ticket import db, Ticket
from backend.utils.validators import validate_json, sanitize_input
from backend.utils.auth_middleware import token_required, admin_required, ticket_admin_required

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/', strict_slashes=False, methods=['GET'])
@token_required
def get_tickets(current_user):
    try:
        query = Ticket.query
        
        # Filtrado por Rol
        if current_user.role == 'Administrador':
            depto_destino = request.args.get('departamento_destino')
            if depto_destino:
                query = query.filter(Ticket.departamento_destino == depto_destino)
        elif current_user.role == 'Admin Data':
            query = query.filter(Ticket.departamento_destino == 'BI')
        elif current_user.role == 'Admin HelpDesk':
            query = query.filter(Ticket.departamento_destino == 'HELPDESK')
        else:
            query = query.filter(Ticket.creator_email == current_user.email)
            depto_destino = request.args.get('departamento_destino')
            if depto_destino:
                query = query.filter(Ticket.departamento_destino == depto_destino)

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
                Ticket.asunto.ilike(search_term),
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
        
        required_fields = ['nombre_solicitante', 'empresa', 'departamento', 'descripcion']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"El campo {field} es requerido"}), 400

        depto_destino = data.get('departamento_destino', 'BI')
        
        # Restricción para Usuario Arturos: Solo permite solicitudes a HelpDesk
        if current_user.role == 'Usuario Arturos' and depto_destino == 'BI':
            return jsonify({"error": "Los usuarios de Arturos solo pueden realizar solicitudes al departamento de HelpDesk"}), 403

        asunto = data.get('asunto') or data['descripcion'][:60]
        
        detalles_adicionales = data.get('detalles_adicionales', {})
        if not isinstance(detalles_adicionales, dict):
            detalles_adicionales = {}

        tipo_solicitud = data.get('tipo_solicitud')
        if depto_destino == 'BI':
            if not tipo_solicitud:
                return jsonify({"error": "El campo tipo_solicitud es requerido para Requerimientos Data"}), 400

        new_ticket = Ticket(
            departamento_destino=depto_destino,
            nombre_solicitante=data['nombre_solicitante'],
            empresa=data['empresa'],
            departamento=data['departamento'],
            asunto=asunto,
            descripcion=data['descripcion'],
            tipo_solicitud=tipo_solicitud,
            detalles_adicionales=detalles_adicionales,
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
@ticket_admin_required
@validate_json
def update_ticket(current_user, ticket_id):
    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket no encontrado"}), 404
            
        if current_user.role == 'Admin Data' and ticket.departamento_destino != 'BI':
            return jsonify({"error": "Acceso denegado: No tiene permisos para gestionar tickets de esta área"}), 403

        if current_user.role == 'Admin HelpDesk' and ticket.departamento_destino != 'HELPDESK':
            return jsonify({"error": "Acceso denegado: No tiene permisos para gestionar tickets de esta área"}), 403
            
        data = sanitize_input(request.get_json())
        
        if 'estado' in data:
            nuevo_estado = data['estado']
            valid_estados = [
                'Creado / Esperando Asignación',
                'Asignado/Desarrollo',
                'Asignado / En progreso',
                'Información Requerida',
                'Pausado',
                'Rechazado/Fuera de Alcance',
                'Cerrado/Resuelto'
            ]
            if nuevo_estado not in valid_estados:
                return jsonify({"error": f"Estado inválido: {nuevo_estado}"}), 400
                
            if nuevo_estado in ['Rechazado/Fuera de Alcance', 'Pausado', 'Información Requerida']:
                if not data.get('motivo_justificacion') and not ticket.motivo_justificacion:
                    return jsonify({"error": "Se requiere motivo de justificación para este estado"}), 400
            
            ticket.estado = nuevo_estado
            
        if 'prioridad' in data:
            valid_priorities = ['Prioridad 1', 'Prioridad 2', 'Prioridad 3', 'Prioridad 4']
            p = data['prioridad']
            if p and p not in valid_priorities:
                return jsonify({"error": "Prioridad inválida"}), 400
            ticket.prioridad = p if p else None
            
        if 'encargado' in data:
            ticket.encargado = data['encargado']
            if 'estado' not in data and ticket.estado == 'Creado / Esperando Asignación':
                ticket.estado = 'Asignado/Desarrollo'
                
        if 'motivo_justificacion' in data:
            ticket.motivo_justificacion = data['motivo_justificacion']

        # Generalización: Asignar tipo_solicitud / caso directamente a la columna tipo_solicitud
        if 'tipo_solicitud' in data or 'caso' in data:
            val = data.get('tipo_solicitud')
            if val is None:
                val = data.get('caso')
            ticket.tipo_solicitud = val

        # Limpiar 'caso' de detalles_adicionales JSONB
        if 'detalles_adicionales' in data or (ticket.detalles_adicionales and 'caso' in ticket.detalles_adicionales):
            current_detalles = dict(ticket.detalles_adicionales or {})
            if 'detalles_adicionales' in data and isinstance(data['detalles_adicionales'], dict):
                current_detalles.update(data['detalles_adicionales'])
            current_detalles.pop('caso', None)
            ticket.detalles_adicionales = current_detalles

        db.session.commit()
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
