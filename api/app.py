from flask import Flask
from flask_jwt_extended import JWTManager
from routes.usuario_routes import usuario_bp
from routes.banco_routes import banco_bp
from routes.simulacao_routes import simulacao_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = 'gui'
    jwt = JWTManager(app)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(banco_bp)
    app.register_blueprint(simulacao_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)