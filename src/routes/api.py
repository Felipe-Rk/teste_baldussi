from flask import Flask
from flask_jwt_extended import JWTManager
from .auth_routes import auth_bp
from .user_routes import user_bp
from .transc_routes import transcription_bp

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Substitua por uma chave segura em produção

    # Registro dos blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(transcription_bp, url_prefix='/transcriptions')

    # Configuração do JWT
    jwt = JWTManager(app)
    
    return app