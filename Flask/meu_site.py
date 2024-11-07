from flask import Flask
from app.controllers.routes import routes_bp
from app.extensions import db
import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv(".gitignore/.env")

# Acessar a senha do banco de dados
database_password = os.getenv("DATABASE_PASSWORD")

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # Configuração da chave secreta e do banco de dados
    app.config['SECRET_KEY'] = "123Salsich@#"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://admin:{database_password}@ong.cnq6aasawjg8.sa-east-1.rds.amazonaws.com/miaumigos"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://BD07032415:Ysios4@BD-ACD/BD07032415"
    
    # Inicializar o SQLAlchemy com o app
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    # Registrar blueprints
    app.register_blueprint(routes_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)