from flask import Flask
from flask_jwt_extended import JWTManager
from src.auth.auth_endpoint import auth_bp  
from src.user.user_endpoint import user_bp 

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  
jwt = JWTManager(app)

# Registrar Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')  
app.register_blueprint(user_bp, url_prefix='/api')  

if __name__ == '__main__':
    app.run(debug=True)