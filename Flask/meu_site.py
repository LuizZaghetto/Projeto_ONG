from flask import Flask
from flask_migrate import Migrate
from app.controllers.routes import routes_bp
from app.extensions import db
import os
from dotenv import load_dotenv
import app.functions as func


# Carregar as variáveis do .env
load_dotenv()

# Acessar a chave secretaos.
secret_key = os.getenv("SECRET_KEY")

# Acessar os dados do banco de dados
# Banco Principal
database_user = os.getenv("DATABASE_USER")
database_host = os.getenv("DATABASE_HOST")
database_password = os.getenv("DATABASE_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
# Banco Secundário
database2_user =os. getenv("DATABASE2_USER")
database2_host = os.getenv("DATABASE2_HOST")
database2_password = os.getenv("DATABASE2_PASSWORD")
database2_name = os.getenv("DATABASE2_NAME")

err = {
    'OperationalError': 'Erro ao conectar ao banco de dados.',
    'KeyError': 'Variável de ambiente ausente.',
    'FileNotFoundError': 'Arquivo de configuração não encontrado.',
    'ValueError': 'Valor inválido fornecido.',
    'RuntimeError': 'Erro de contexto de aplicação.',
}

def create_app():
    try:
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        
        # Configuração da chave secreta e do banco de dados
        app.config['SECRET_KEY'] = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{database_user}:{database_password}@{database_host}/{database_name}"
        #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{database2_user}:{database2_password}@{database2_host}/{database2_name}"

        # Pasta de migrações personalizada
        app.config['MIGRATION_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'migrations')
        
        # Inicializar o SQLAlchemy com o app
        db.init_app(app)

        #Inicializar o Migrate com o app e db
        migrate = Migrate(app, db, directory=app.config['MIGRATION_DIR'])

        with app.app_context():
            db.create_all()
            # func.atualizar_dados_formatados()

        
        # Registrar blueprints
        app.register_blueprint(routes_bp)


            
        return app
    except Exception as e:
        error_name = e.__class__.__name__
        if error_name in err.keys():
            print(err[error_name])



app = create_app()
if __name__ == "__main__": 
    app.run(debug = True)