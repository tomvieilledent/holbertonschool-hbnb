#!/usr/bin/python3

import os
from flask import Flask, Blueprint, send_file
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__, static_folder='frontend', static_url_path='/assets')
    app.config.from_object(config_class)

    # Activer CORS pour toutes les routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    # Créer un blueprint pour servir le frontend
    frontend_bp = Blueprint('frontend', __name__)

    @frontend_bp.route('/')
    @frontend_bp.route('/index.html')
    def index():
        frontend_path = os.path.join(os.path.dirname(
            __file__), 'frontend', 'index.html')
        with open(frontend_path, 'r', encoding='utf-8') as f:
            return f.read()

    # Servir les fichiers statiques du frontend
    @frontend_bp.route('/style.css')
    def serve_css():
        return send_file(os.path.join('frontend', 'style.css'), mimetype='text/css')

    @frontend_bp.route('/images/<path:filename>')
    def serve_images(filename):
        return send_file(os.path.join('frontend', 'images', filename))

    app.register_blueprint(frontend_bp)

    authorizations = {
        'BearerAuth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT token: Bearer <token>'
        }
    }

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/docs",
        authorizations=authorizations,
        security='BearerAuth'
    )

    # Register API namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    with app.app_context():
        db.create_all()

    bcrypt.init_app(app)
    jwt.init_app(app)
    return app
