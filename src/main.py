from flask import Flask
from flask_jwt_extended import JWTManager
from src.auth.auth_endpoint import auth_bp
from src.user.user_endpoint import user_bp
from src.transcription.transc_endpoint import transcription_bp
app = Flask(__name__)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "super-secret" # Use uma chave segura em produção
jwt = JWTManager(app)


# Registra o Blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth') # Prefixo opcional
app.register_blueprint(user_bp)
app.register_blueprint(transcription_bp, url_prefix='/transcriptions')

if __name__ == "__main__":
    app.run(debug=True)