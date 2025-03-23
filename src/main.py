from flask import Flask
from flask_jwt_extended import JWTManager
from src.auth.auth_endpoint import auth_bp  # Importe o Blueprint de autenticação

app = Flask(__name__)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "super-secret"  # Use uma chave segura em produção
jwt = JWTManager(app)

# Registra o Blueprint de autenticação
app.register_blueprint(auth_bp, url_prefix='/auth')  # Prefixo opcional

if __name__ == "__main__":
    app.run(debug=True)