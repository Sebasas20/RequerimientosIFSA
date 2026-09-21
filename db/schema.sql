-- db/schema.sql
DO $$ BEGIN
    CREATE TYPE ticket_estado AS ENUM (
        'Creado / Esperando Asignación',
        'Asignado/Desarrollo',
        'Información Requerida',
        'Pausado',
        'Rechazado/Fuera de Alcance'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

DO $$ BEGIN
    CREATE TYPE ticket_prioridad AS ENUM (
        'Prioridad 1',
        'Prioridad 2',
        'Prioridad 3',
        'Prioridad 4'
    );
EXCEPTION WHEN duplicate_object THEN null; END $$;

CREATE TABLE IF NOT EXISTS requirement_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    departamento_destino VARCHAR(50) NOT NULL DEFAULT 'BI',
    nombre_solicitante VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    departamento VARCHAR(255) NOT NULL,
    asunto VARCHAR(255),
    descripcion TEXT NOT NULL,
    tipo_solicitud VARCHAR(255),
    detalles_adicionales JSONB DEFAULT '{}'::jsonb,
    estado ticket_estado NOT NULL DEFAULT 'Creado / Esperando Asignación',
    prioridad ticket_prioridad,
    encargado VARCHAR(255),
    motivo_justificacion TEXT,
    creator_email VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_req_tickets_depto_destino ON requirement_tickets(departamento_destino);
CREATE INDEX IF NOT EXISTS idx_req_tickets_estado ON requirement_tickets(estado);
CREATE INDEX IF NOT EXISTS idx_req_tickets_departamento ON requirement_tickets(departamento);
CREATE INDEX IF NOT EXISTS idx_req_tickets_created_at ON requirement_tickets(created_at);
