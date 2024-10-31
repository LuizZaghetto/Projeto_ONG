from flask import Flask, render_template, abort, flash
from app.controllers.routes import routes_bp
from app.extensions import db
import json

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # Configuração da chave secreta e do banco de dados
    app.config['SECRET_KEY'] = "123Salsich@#"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123Salsich%40#@localhost/ong'
    
    # Inicializar o SQLAlchemy com o app
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(routes_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)