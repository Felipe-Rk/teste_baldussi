from flask import Flask
import atexit
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from .auth_routes import auth_bp
from .user_routes import user_bp
from .transc_routes import transcription_bp
from src.database.mysql.mysql_config import setup_mysql_database
from src.database.mongo.mongo_config import setup_mongo_database

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"  # Substitua por uma chave segura em produção
    
    setup_mysql_database()
    setup_mongo_database()

    # Inicializar Swagger
    swagger = Swagger(app) #http://127.0.0.1:5000/apidocs/#/

    # Registro dos blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(transcription_bp, url_prefix='/transcriptions')

    # Configuração do JWT
    jwt = JWTManager(app)

    return app

from src.database.mysql.mysql import mysql_connection
from src.database.mongo.mongo import mongo_client

def close_connections():
    if mysql_connection:
        print("🔹 Fechando conexão MySQL...")
        mysql_connection.close()
    if mongo_client:
        print("🔹 Fechando conexão MongoDB...")
        mongo_client.close()

atexit.register(close_connections)