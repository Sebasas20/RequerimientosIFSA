
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()

class Ticket(db.Model):
    __tablename__ = 'requirement_tickets'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_solicitante = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(255), nullable=False)
    departamento = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo_solicitud = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='Creado / Esperando Asignación')
    prioridad = db.Column(db.String(50), nullable=True)
    encargado = db.Column(db.String(255), nullable=True)
    motivo_justificacion = db.Column(db.Text, nullable=True)
    creator_email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_solicitante': self.nombre_solicitante,
            'empresa': self.empresa,
            'departamento': self.departamento,
            'descripcion': self.descripcion,
            'tipo_solicitud': self.tipo_solicitud,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'encargado': self.encargado,
            'motivo_justificacion': self.motivo_justificacion,
            'creator_email': self.creator_email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
