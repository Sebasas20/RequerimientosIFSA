from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from backend.models.ticket import db
import backend.models.encargado
import backend.models.categoria
from backend.models.categoria import Categoria
from backend.routes.auth import auth_bp
from backend.routes.users import users_bp
from backend.routes.tickets import tickets_bp
from backend.routes.encargados import encargados_bp
from backend.routes.categorias import categorias_bp

def seed_initial_categories():
    initial_bi = [
        'Creación de Dashboards',
        'Análisis profundo',
        'Modelos Estadísticos/ML',
        'Troubleshooting',
        'Otros requerimientos'
    ]
    initial_helpdesk = [
        'Impresión de Facturas',
        'Factura Duplicada',
        'Odoo',
        'Merchant',
        'Printer Fiscal',
        'Confirmación de Zelle',
        'Diferencia Fiscal',
        'Gerencia',
        'Error en el Formato de Impresión de la Factura',
        'Biométrico',
        'Conexión con Bases de Datos',
        'POS de venta',
        'Error en el Contenido de la Factura',
        'Conexión de Red',
        'Impresora',
        'Otros'
    ]

    for cat_name in initial_bi:
        if not Categoria.query.filter_by(nombre=cat_name, departamento_destino='BI').first():
            db.session.add(Categoria(nombre=cat_name, departamento_destino='BI'))

    for cat_name in initial_helpdesk:
        if not Categoria.query.filter_by(nombre=cat_name, departamento_destino='HELPDESK').first():
            db.session.add(Categoria(nombre=cat_name, departamento_destino='HELPDESK'))

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS - based on ALLOWED_ORIGINS in .env
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_initial_categories()

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
    app.register_blueprint(encargados_bp, url_prefix='/api/encargados')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')

    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
