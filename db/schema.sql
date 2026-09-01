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
    nombre_solicitante VARCHAR(255) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    departamento VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    tipo_solicitud VARCHAR(255) NOT NULL CHECK (
        tipo_solicitud IN ('Creación de Dashboards', 'Análisis profundo', 'Modelos Estadísticos/ML', 'Troubleshooting', 'Otros requerimientos')
    ),
    estado ticket_estado NOT NULL DEFAULT 'Creado / Esperando Asignación',
    prioridad ticket_prioridad,
    encargado VARCHAR(255),
    motivo_justificacion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_req_tickets_estado ON requirement_tickets(estado);
CREATE INDEX IF NOT EXISTS idx_req_tickets_departamento ON requirement_tickets(departamento);
CREATE INDEX IF NOT EXISTS idx_req_tickets_created_at ON requirement_tickets(created_at);
CREATE INDEX IF NOT EXISTS idx_req_tickets_tipo_solicitud ON requirement_tickets(tipo_solicitud);
