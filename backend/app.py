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

def ensure_enum_values():
    try:
        values = ['Cerrado/Resuelto', 'Cerrado / Resuelto', 'Asignado / En progreso']
        for val in values:
            try:
                db.session.execute(db.text(f"ALTER TYPE ticket_estado ADD VALUE IF NOT EXISTS '{val}';"))
                db.session.commit()
            except Exception:
                db.session.rollback()
    except Exception:
        pass

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure CORS - based on ALLOWED_ORIGINS in .env
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    db.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_enum_values()

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
